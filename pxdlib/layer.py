'''
Layer objects, bound to a PXD file.
'''

import json
import plistlib
import base64
from io import UnsupportedOperation

from .structure import blob, make_blob, vercon, verlist
from .enums import LayerFlag, BlendMode, LayerTag


class Layer:
    def __init__(self, pxd, ID):
        self._pxd = pxd
        self._id = ID

        self._uuid, = pxd._db.execute(
            f"select identifier from document_layers where id = {ID};"
        ).fetchone()

        self._info = dict(pxd._db.execute(
            f"select key, value from layer_info where layer_id = {ID};"
        ).fetchall())

    def __repr__(self):
        return f'<{type(self).__name__} {repr(self.name)}>'

    def _setinfo(self, key, data):
        if self._pxd.closed:
            raise UnsupportedOperation('not writable')
        self._info[key] = data
        c = self._pxd._db.cursor()
        c.execute(
            'update layer_info set value = ?'
            'where layer_id = ? and key = ?',
            (data, self._id, key)
        )

    # Attributes

    @property
    def name(self) -> str:
        '''
        The layer's given visible name.
        '''
        return blob(self._info['name'])

    @name.setter
    def name(self, name: str):
        name = name or "Layer"
        self._setinfo('name', make_blob(b'Strn', name))
        # Manually setting a name means Pixelmator no longer auto-sets name,
        # if a text layer
        DYNAMIC = 'text-nameIsDynamic'
        if DYNAMIC in self._info:
            self._setinfo(DYNAMIC, make_blob(b'SI16', 0))

    @property
    def opacity(self) -> int:
        '''
        The layer's opacity, from 0 to 100.
        '''
        return blob(self._info['opacity'])

    @opacity.setter
    def opacity(self, opacity):
        if isinstance(opacity, int) and 0 <= opacity <= 100:
            self._setinfo('opacity', make_blob(b'LOpc', opacity))
        else:
            raise TypeError('Opacity must be an integer in range [0, 100].')

    @property
    def position(self) -> tuple:
        '''
        The position of the layer (defined as its center).
        '''
        return tuple(blob(self._info['position']))

    @position.setter
    def position(self, pos):
        x, y = pos
        self._setinfo('position', make_blob(b'PTPt', x, y))

    @property
    def size(self) -> int:
        '''
        The position of the layer (defined as its center).
        '''
        return tuple(blob(self._info['size']))

    @size.setter
    def size(self, size):
        w, h = size
        self._setinfo('size', make_blob(b'PTSz', w, h))

    @property
    def angle(self) -> float:
        '''
        The angle of a (text) layer in degrees.

        A float in the range [0, 360).
        '''
        return blob(self._info['angle']) % 360

    @angle.setter
    def angle(self, angle):
        self._setinfo('angle', make_blob(b'PTFl', angle % 360))

    @property
    def blendMode(self) -> BlendMode:
        '''
        The blending mode of the layer.
        '''
        return BlendMode(blob(self._info['blendMode']))

    @blendMode.setter
    def blendMode(self, blend):
        if not isinstance(blend, BlendMode):
            raise TypeError('Blend mode must be a BlendMode.')
        self._setinfo('blendMode', make_blob(b'Blnd', str(blend)))

    @property
    def tag(self) -> LayerTag:
        '''
        The blending mode of the layer.
        '''
        return LayerTag(self._info['color-value'])

    @tag.setter
    def tag(self, tag):
        blend = blend or LayerTag.none
        if not isinstance(blend, LayerTag):
            raise TypeError('Tag must be a LayerTag.')
        self._setinfo('color-value', int(tag))

    # Flags

    @property
    def _flags(self) -> LayerFlag:
        return LayerFlag(blob(self._info['flags']))

    @_flags.setter
    def _flags(self, val: LayerFlag):
        self._setinfo('flags', make_blob(b'UI64', int(val)))

    def _flag_set(self, flag, truth):
        past_truth = bool(self._flags & flag)
        print(truth, past_truth)
        if truth != past_truth:
            # flip the bit
            self._flags ^= flag

    @property
    def is_visible(self):
        return bool(self._flags & LayerFlag.visible)

    @is_visible.setter
    def is_visible(self, val):
        self._flag_set(LayerFlag.visible, bool(val))

    @property
    def is_locked(self):
        return bool(self._flags & LayerFlag.locked)

    @is_locked.setter
    def is_locked(self, val):
        self._flag_set(LayerFlag.locked, bool(val))

    @property
    def is_clipping(self):
        return bool(self._flags & LayerFlag.clipping)

    @is_clipping.setter
    def is_clipping(self, val):
        self._flag_set(LayerFlag.clipping, bool(val))

    @property
    def is_mask(self):
        return bool(self._flags & LayerFlag.mask)

    @is_mask.setter
    def is_mask(self, val):
        self._flag_set(LayerFlag.mask, bool(val))


class GroupLayer(Layer):
    @property
    def children(self):
        '''
        The children of the group layer.
        '''
        # TODO: avoid giving the mask, if any
        return self._pxd._layers(self)

    def all_layers(self):
        return self._pxd._layers(self, recurse=True)


class VectorLayer(Layer):
    pass


class RasterLayer(Layer):
    pass


class TextLayer(Layer):
    def __init__(self, pxd, ID):
        Layer.__init__(self, pxd, ID)
        data = vercon(json.loads(self._info['text-stringData']))
        data = base64.b64decode(data['stringNSCodingData'])
        self._text = plistlib.loads(data)['$objects']

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
