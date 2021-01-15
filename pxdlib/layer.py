'''
Layer objects, bound to a PXD file.
'''

import json
import plistlib
import base64
from io import UnsupportedOperation

from .helpers import uuid
from .structure import blob, make_blob, verb
from .enums import LayerFlag, BlendMode, LayerTag
from .styles import _STYLES
from .errors import ChildError, MaskError, StyleError


class Layer:
    __slots__ = ('pxd', '_id')

    def __init__(self, parent, ID=None):
        if type(self) is Layer:
            raise TypeError('Cannot instantiate a bare Layer.')

        if isinstance(parent, Layer):
            self.pxd = parent.pxd
        else:
            self.pxd = parent

        if isinstance(ID, int):
            self._id = ID
        else:
            self._create(parent)

    def _create(self, parent):
        self._id = self._new_entry(parent, type(self))
        self.pxd._layer_cache[self._id] = self

        self._assert(write=True)

        def tag(k, kind, *vals):
            if kind is None:
                blob = vals[0]
            else:
                blob = make_blob(kind, *vals)
            self._setinfo(k, blob, create=True)

        if isinstance(self, TextLayer):
            tag('text-nameIsDynamic', b'SI16', 0)

        tag('opacity', b'LOpc', 100)
        tag('color-value', None, 0)
        tag('blendMode', b'Blnd', 'norm')

        if isinstance(self, RasterLayer):
            tag('flags', b'UI64', 0b1000001)
        else:
            tag('flags', b'UI64', 0b0000001)

        if isinstance(self, GroupLayer):
            tag('name', b'Strn', 'New Group')
        elif isinstance(self, TextLayer):
            tag('name', b'Strn', 'Text')
        else:
            tag('name', b'Strn', 'Layer')

        tag('angle', b'PTFl', 0)

    def _new_entry(self, parent, kind, index_at_parent=0):
        '''
        internal: create entry and get ID. doesn't set info!
        '''
        # note that here, pxd is not necessarily self.pxd
        # (this is also used when copying to a different pxd)
        if isinstance(parent, Layer):
            pxd = parent.pxd
            parent_UUID = parent._uuid
        else:
            pxd = parent
            parent_UUID = None

        if pxd.closed:
            raise UnsupportedOperation('not writable')

        UUID = uuid()
        for code, kind in _LAYER_TYPES.items():
            if isinstance(self, kind):
                break
        else:
            raise TypeError('Unknown type copied')
        return pxd._db.execute(
            'insert into document_layers'
            ' (identifier, parent_identifier, index_at_parent, type)'
            ' values (?, ?, ?, ?)',
            (UUID, parent_UUID, index_at_parent, code)
        ).lastrowid
        return id

    @property
    def _uuid(self):
        return self.pxd._db.execute(
            f"select identifier from document_layers where id = {self._id};"
        ).fetchone()[0]

    def _assert(self, write=False):
        if self._id is None:
            raise UnsupportedOperation('not readable')
        if write and self.pxd.closed:
            raise UnsupportedOperation('not writable')

    @property
    def parent(self):
        '''The parent, which may be a Layer or a PXDFile.'''
        # construct {child: parent} and fetch
        children = dict(self.pxd._db.execute(
            'select child.id, parent.id from ('
            '  document_layers child inner join document_layers parent'
            '  on child.parent_identifier = parent.identifier);'
        ).fetchall())
        if self._id not in children:
            return self.pxd
        return self.pxd._layer(children[self._id])

    @parent.setter
    def parent(self, val):
        self._assert(write=True)
        if val is None or val is self.pxd:
            uuid = None
        elif isinstance(val, Layer):
            uuid = val._uuid

        if self.is_mask:
            raise MaskError(
                "Cannot set mask's parent."
                " Try setting `layer.mask = mask` instead.")

        # disallow if val would be a non-mask on a non-group!
        can_hold_non_mask = uuid == None or isinstance(val, GroupLayer)

        if not can_hold_non_mask:
            raise ChildError('Invalid parent (must be GroupLayer or ')

        if val.pxd is self.pxd:
            # intra-PXD
            self.pxd._db.execute(
                'update document_layers set parent_identifier = ?'
                'where id = ?;',
                (uuid, self._id)
            )
        else:
            # inter-PXD
            if val.pxd.closed:
                raise UnsupportedOperation('not writable')
            new = self._copyto(val, asmask=False, keep_index=False)
            self.delete()
            self.pxd = new.pxd
            self._id = new._id
            self.pxd._layer_cache[self._id] = self
            del new

    @property
    def mask(self):
        '''
        The layer's mask, if any.

        If you set a mask, it will delete the current one.
        If you set a mask to an existing layer, it will move it from
        its original position.
        '''
        self._assert()
        for layer in self.pxd._layers(self):
            if layer.is_mask:
                return layer
        else:
            return None

    @mask.setter
    def mask(self, mask):
        self._assert(write=True)
        if not isinstance(mask, RasterLayer):
            raise MaskError('Only RasterLayers can be masks.')
        if self.mask:
            self.mask.delete()

        mask.parent = self
        mask._flag_set(LayerFlag.mask, True)

    def delete(self):
        '''
        Irrevocably delete layer and children.

        Note that no attributes can be read or written after this is done.
        '''
        if self._id is None:
            return
        if self.pxd.closed:
            raise UnsupportedOperation('not writable')

        for child in self.pxd._layers(self):
            child.delete()

        ID = self._id
        self._id = None

        del self.pxd._layer_cache[ID]
        self.pxd._db.execute(
            f'delete from layer_info where layer_id = {ID};'
        )
        self.pxd._db.execute(
            f'delete from layer_tiles where layer_id = {ID};'
        )
        self.pxd._db.execute(
            f'delete from document_layers where id = {ID};'
        )

    def _contains(self, child):
        return child in self.pxd._layers(self, recurse=True)

    def copyto(self, parent, asmask=False):
        return self._copyto(parent, asmask, False)

    def _copyto(self, parent, asmask, keep_index):
        if self is parent or self._contains(parent):
            raise ValueError(
                'Cannot copy layer into child.'
            )
        if isinstance(parent, Layer):
            if asmask and parent.mask is not None:
                raise MaskError('This layer already has a mask.')
            destpxd = parent.pxd
        else:
            if asmask:
                raise MaskError('Only Layers can have masks.')
            destpxd = parent

        self._assert()

        index_at_parent = 0
        if keep_index:
            index_at_parent, = self.pxd._db.execute(
                'select index_at_parent from document_layers'
                f' where id = {self._id}'
            ).fetchone()

        ID = self._new_entry(parent, type(self), index_at_parent)

        info = self.pxd._db.execute(
            'select key, value from layer_info'
            f' where layer_id = {self._id};',
        ).fetchall()
        for k, v in info:
            destpxd._db.execute(
                'insert into layer_info'
                ' (layer_id, key, value)'
                ' values (?, ?, ?)',
                (ID, k, v)
            )

        layer = destpxd._layer(ID)
        if asmask:
            layer.is_mask = True
        for child in self.pxd._layers(self):
            self._copyto(layer, asmask=False, keep_index=True)

        return layer

    def __repr__(self):
        typ = type(self).__name__
        if self._id is None:
            return f'<{typ}: deleted layer>'
        name = repr(self.name)
        info = []
        if self.is_mask:
            name = f'mask of {repr(self.parent.name)}'
        if self.tag:
            info.append(self.tag.name)
        if info:
            info = f" ({', '.join(info)})"
        else:
            info = ""
        return f'<{typ} {name}{info}>'

    def _info(self, key, default=None):
        self._assert()
        value = self.pxd._db.execute(
            "select value from layer_info"
            f" where layer_id = ? and key = ?;",
            (self._id, key)
        ).fetchone()
        if value is None:
            return default
        return value[0]

    def _setinfo(self, key, data, create=False):
        self._assert(write=True)
        if create:
            self.pxd._db.execute(
                'insert into layer_info'
                ' (layer_id, key, value)'
                ' values (?, ?, ?);',
                (self._id, key, data)
            )
        else:
            self.pxd._db.execute(
                'update layer_info set value = ?'
                ' where layer_id = ? and key = ?',
                (data, self._id, key)
            )

    # Attributes

    @property
    def name(self) -> str:
        '''
        The layer's given visible name.
        '''
        return blob(self._info('name'))

    @name.setter
    def name(self, name: str):
        name = name or "Layer"
        self._setinfo('name', make_blob(b'Strn', name))
        # Manually setting a name means Pixelmator no longer auto-sets name,
        # if a text layer
        DYNAMIC = 'text-nameIsDynamic'
        if self._info(DYNAMIC, False):
            self._setinfo(DYNAMIC, make_blob(b'SI16', 0))

    @property
    def opacity(self) -> int:
        '''
        The layer's opacity, an integer from 0 to 100.
        '''
        return blob(self._info('opacity'))

    @opacity.setter
    def opacity(self, opacity):
        if isinstance(opacity, int) and 0 <= opacity <= 100:
            self._setinfo('opacity', make_blob(b'LOpc', opacity))
        else:
            raise TypeError('Opacity must be an integer in range [0, 100].')

    @property
    def position(self) -> tuple:
        '''
        The center of the layer, defined in (x, y) pixels such that
        the origin is at the bottom left.
        '''
        return tuple(blob(self._info('position')))

    @position.setter
    def position(self, pos):
        x, y = pos
        self._setinfo('position', make_blob(b'PTPt', x, y))

    @property
    def size(self) -> int:
        '''
        The position of the layer (defined as its center).
        '''
        return tuple(blob(self._info('size')))

    @size.setter
    def size(self, size):
        w, h = size
        self._setinfo('size', make_blob(b'PTSz', w, h))

    @property
    def angle(self) -> float:
        '''
        The angle of a (text) layer as a float in degrees.

        Nominally 0 except for text layers.
        '''
        return blob(self._info('angle')) % 360

    @angle.setter
    def angle(self, angle):
        self._setinfo('angle', make_blob(b'PTFl', angle % 360))

    @property
    def blendMode(self) -> BlendMode:
        '''
        The blending mode of the layer.
        '''
        return BlendMode(blob(self._info('blendMode')))

    @blendMode.setter
    def blendMode(self, blend):
        if not isinstance(blend, BlendMode):
            raise TypeError('Blend mode must be a BlendMode.')
        self._setinfo('blendMode', make_blob(b'Blnd', str(blend)))

    @property
    def tag(self) -> LayerTag:
        '''
        The color tag for the layer.
        '''
        return LayerTag(self._info('color-value'))

    @tag.setter
    def tag(self, tag):
        tag = tag or LayerTag.none
        if not isinstance(tag, LayerTag):
            raise TypeError('Tag must be a LayerTag.')
        self._setinfo('color-value', int(tag))

    # Flags

    @property
    def _flags(self) -> LayerFlag:
        return LayerFlag(blob(self._info('flags')))

    @_flags.setter
    def _flags(self, val: LayerFlag):
        self._setinfo('flags', make_blob(b'UI64', int(val)))

    def _flag_set(self, flag, truth):
        past_truth = bool(self._flags & flag)
        if truth != past_truth:
            # flip the bit
            self._flags ^= flag

    @property
    def is_visible(self) -> bool:
        '''
        A boolean defining if the layer is visible.
        '''
        return bool(self._flags & LayerFlag.visible)

    @is_visible.setter
    def is_visible(self, val: bool):
        self._flag_set(LayerFlag.visible, bool(val))

    @property
    def is_locked(self) -> bool:
        '''
        A boolean defining if the layer is user-locked.

        This does not affect if `pxdlib` can modify it though :)
        '''
        return bool(self._flags & LayerFlag.locked)

    @is_locked.setter
    def is_locked(self, val: bool):
        self._flag_set(LayerFlag.locked, bool(val))

    @property
    def is_clipping(self) -> bool:
        '''
        A boolean defining if the layer is a clipping mask.
        '''
        return bool(self._flags & LayerFlag.clipping)

    @is_clipping.setter
    def is_clipping(self, val: bool):
        self._flag_set(LayerFlag.clipping, bool(val))

    @property
    def is_mask(self) -> bool:
        '''
        A boolean defining if the layer is a mask.

        This may raise a MaskError if it would put the layer
        in a illogical situation: layers can only have one mask,
        and not all layers can have non-mask children.
        '''
        return bool(self._flags & LayerFlag.mask)

    @is_mask.setter
    def is_mask(self, masked: bool):
        not_group = (
            isinstance(self.parent, Layer)
            and not isinstance(self.parent, GroupLayer)
        )
        if not masked and not_group:
            raise MaskError(
                'Cannot unmask a layer: would not be a valid child. '
                'Consider setting `layer.parent`.')
        elif masked and not isinstance(self, RasterLayer):
            raise MaskError('Only RasterLayers can be masks.')
        elif masked and self.parent.mask is not None:
            raise MaskError(
                "The layer's parent already has a mask. "
                'Consider setting `layer.parent`.'
            )

        self._flag_set(LayerFlag.mask, bool(val))

    @property
    def styles(self):
        '''
        A list of Style objects applied to the layer, in the order applied.

        Note that this must be extracted and set. For example:

            layer.styles[0].opacity = 0

        would not have any effect.
        '''
        data = self._info('styles-data')
        if data is None:
            return []
        data = verb(json.loads(data.decode()))
        assert data['csr'] == 0
        styles = []
        for k in 'fsiS':
            kind = _STYLES[k]
            for style in data[k]:
                style = kind._from_layer(verb(style))
                styles.append(style)
        return styles

    @styles.setter
    def styles(self, val: list):
        if isinstance(self, GroupLayer):
            raise StyleError('GroupLayers cannot have styles.')
        # attempt to extract csr, ctx
        data = self._info('styles-data', None)
        if data is None:
            create = True
            data = {}
        else:
            create = False
            data = verb(json.loads(data.decode()))
        data['csr'] = 0
        for k in 'fsiS':
            data[k] = []
        for style in val:
            k = style._tag
            style = style._to_layer()
            data[k].append([1, style])
        data = json.dumps([1, data]).encode()
        self._setinfo('styles-data', data, create=create)


class GroupLayer(Layer):
    @property
    def children(self):
        '''
        The children of the group layer,
        excluding any masks.
        '''
        return [
            layer for layer in self.pxd._layers(self)
            if not layer.is_mask
        ]

    def all_layers(self):
        return self.pxd._layers(self, recurse=True)


class VectorLayer(Layer):
    pass


class RasterLayer(Layer):
    pass


class TextLayer(Layer):
    @property
    def _text(self):
        data = verb(json.loads(self._info('text-stringData')))
        data = base64.b64decode(data['stringNSCodingData'])
        return plistlib.loads(data)['$objects']

    def getText(self):
        '''
        Get (unformatted) text contents.
        '''

        pText = self._text[1]['NSString']
        return self._text[pText]['NS.string']


_LAYER_TYPES = {
    1: RasterLayer,
    2: TextLayer,
    3: VectorLayer,
    4: GroupLayer
}
