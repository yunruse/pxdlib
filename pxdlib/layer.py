'''
Layer objects, bound to a PXD file.
'''

from .structure import blob, make_blob


class Layer:
    # Info layers with known types that can be modified and removed.
    KEYS = {
        'opacity': b'cpOL',
        'position': b'tPTP',
        'size': b'zSTP'
    }

    def __init__(self, pxd, ID):
        self._pxd = pxd
        self._id = ID

        self._uuid, = pxd.db.execute(
            f"select identifier from document_layers where id = {ID};"
        ).fetchone()

        self._info = dict(pxd.db.execute(
            f"select key, value from layer_info where layer_id = {ID};"
        ).fetchall())

        self.name = blob(self._info['name'])

    def children(self, recurse=False):
        return self._pxd.layers(self._uuid, recurse=recurse)

    def __repr__(self):
        return f'<Layer {repr(self.name)}>'

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
        self._info[key] = data
        c = self._pxd.db.cursor()
        c.execute(
            'update layer_info set value = ?'
            'where layer_id = ? and key = ?',
            (data, self._id, key)
        )


class GroupLayer(Layer):
    pass


class VectorLayer(Layer):
    pass


class RasterLayer(Layer):
    pass


class TextLayer(Layer):
    pass


_LAYER_TYPES = {
    1: RasterLayer,
    2: TextLayer,
    3: VectorLayer,
    4: GroupLayer
}
