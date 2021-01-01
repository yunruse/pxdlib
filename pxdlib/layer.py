'''
Layer objects, bound to a PXD file.
'''

import json
import plistlib
import base64
from io import UnsupportedOperation

from .structure import blob, make_blob, vercon, verlist


class Layer:
    # Info layers with known types that can be modified and removed.
    KEYS = {
        'opacity': b'LOpc',
        'position': b'PTPt',
        'size': b'PTSz'
    }

    def __init__(self, pxd, ID):
        self._pxd = pxd
        self._id = ID

        self._uuid, = pxd._db.execute(
            f"select identifier from document_layers where id = {ID};"
        ).fetchone()

        self._info = dict(pxd._db.execute(
            f"select key, value from layer_info where layer_id = {ID};"
        ).fetchall())

    @property
    def name(self):
        '''
        The layer's given visible name.
        '''
        return blob(self._info['name'])

    @name.setter
    def name(self, name):
        name = name or "Layer"
        self._setinfo('name', make_blob(b'Strn', name))
        # Manually setting a name means Pixelmator no longer auto-sets name,
        # if a text layer
        DYNAMIC = 'text-nameIsDynamic'
        if DYNAMIC in self._info:
            self._setinfo(DYNAMIC, make_blob(b'SI16', 0))

    def __repr__(self):
        return f'<{type(self).__name__} {repr(self.name)}>'

    def __getattr__(self, key):
        kind = self.KEYS.get(key)
        if not kind:
            raise AttributeError
        return blob(self._info[key])

    def __setattr__(self, key, val):
        kind = self.KEYS.get(key)
        if not kind:
            return object.__setattr__(self, key, val)

        try:
            data = make_blob(kind, *val)
        except TypeError:
            data = make_blob(kind, val)
        self._setinfo(key, data)

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
