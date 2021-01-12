'''
PXDFile class, handling most database access.
'''

from pathlib import Path
import sqlite3
from io import UnsupportedOperation
from collections import namedtuple

from .layer import _LAYER_TYPES, Layer
from .structure import blob, make_blob

guides = namedtuple('guides', ('horizontal', 'vertical'))


class PXDFile:
    def __repr__(self):
        return f"PXDFile({repr(str(self.path))})"

    def __init__(self, path):
        self.path = Path(path)
        self._db = sqlite3.connect(self.path / 'metadata.info')
        self._closed = True
        self._layer_cache = {}

        def keyval(table):
            return dict(self._db.execute(
                f"select key, value from {table};"
            ).fetchall())
        self._meta = keyval('document_meta')
        self._info = keyval('document_info')

    # Layer management

    def _layer(self, ID):
        if ID in self._layer_cache:
            return self._layer_cache[ID]
        typ, = self._db.execute(
            f"select type from document_layers where id = {ID};"
        ).fetchone()
        layer = _LAYER_TYPES[typ](self, ID)
        self._layer_cache[ID] = layer
        return layer

    def _layers(self, parent=None, recurse=False):
        '''
        Return a list of layers that are children of the ID given.
        Give no ID to get the top-level layers.
        Specify recurse=True to get children recursively.
        Layers are always given in the user-visible order.
        '''
        if parent is None:
            cond = 'is null'
        elif isinstance(parent, Layer):
            cond = f' = "{parent._uuid}"'
        elif isinstance(parent, str):
            cond = f' = "{parent}"'
        else:
            raise TypeError('ID must be a layer, UUID or None.')

        children = [self._layer(ID) for (ID, ) in self._db.execute(
            "select id from document_layers"
            f" where parent_identifier {cond}"
            " order by index_at_parent asc;",
        ).fetchall()]
        if recurse:
            tree = []
            for child in children:
                tree.append(child)
                tree += self._layers(child._uuid, recurse=True)
            return tree
        else:
            return children

    def layer_with_name(self, name):
        '''Get the first layer found with the given name.'''
        layers = [
            l for l in self._layers(recurse=True)
            if l.name == name
        ]
        return layers[0]

    @property
    def children(self):
        return self._layers()

    def all_layers(self) -> list:
        return self._layers(recurse=True)

    # Database management

    def open(self) -> None:
        '''
        Starts a transaction to modify the document.

        Changes will only be made on `close()`.
        '''
        if not self._closed:
            return
        self._db.execute('PRAGMA journal_mode=DELETE')
        self._db.execute('begin exclusive')
        self._closed = False

    def close(self) -> None:
        '''
        Closes a transaction and commits any changes made.
        '''
        if self._closed:
            return
        self._closed = True
        self._db.execute('commit')

    @property
    def closed(self):
        return self._closed

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self._db.close()

    def _set(self, key, data, is_meta=False):
        if self.closed:
            raise UnsupportedOperation('not writable')
        table = 'document_meta' if is_meta else 'document_info'
        store = self._meta if is_meta else self._info

        store[key] = data
        c = self._db.cursor()
        c.execute(
            f'update {table} '
            'set value = ? where key = ?',
            (data, key)
        )

    # Metadata

    @property
    def guides(self):
        '''
        A list of the guides used for visual alignment.

        Given as the list of horizontal guides (0 = left)
        followed by vertical guides (0 = top).
        '''
        data = [blob(b) for b in blob(self._info['guides'])]
        return guides(
            [r for _, r, vert in data if not vert],
            [r for _, r, vert in data if vert]
        )

    @guides.setter
    def guides(self, guides):
        hor, ver = guides
        guides = [(0, r) for r in hor] + [(1, r) for r in ver]
        data = make_blob(b'Arry', [
            make_blob(b'Guid', 1, int(r), vert)
            for (vert, r) in guides
        ])
        self._set('guides', data)

    @property
    def rulerOrigin(self):
        '''
        The origin of the (visual) ruler.
        '''
        return blob(self._info['rulers-origin'])

    @rulerOrigin.setter
    def rulerOrigin(self, origin):
        x, y = origin
        self._set('rulers-origin', make_blob(b'PTPt', x, y))
