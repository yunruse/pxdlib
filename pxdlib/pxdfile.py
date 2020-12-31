'''
PXDFile class, handling most database access.
'''

from pathlib import Path
import sqlite3

from .layer import _LAYER_TYPES, Layer


class PXDFile:
    def __repr__(self):
        return f"PXDFile({self.path})"

    def __init__(self, path):
        self.path = Path(path)
        self.db = sqlite3.connect(self.path / 'metadata.info')

        def keyval(table):
            return dict(self.db.execute(
                f"select key, value from {table};"
            ).fetchall())
        self._meta = keyval('document_meta')
        self._info = keyval('document_info')

    def _layer(self, ID):
        typ, = self.db.execute(
            f"select type from document_layers where id = {ID};"
        ).fetchone()
        return _LAYER_TYPES[typ](self, ID)

    def layers(self, parent=None, recurse=False):
        '''
        Return a list of layers that are children of the ID given.
        Give no ID to get the top-level layers.
        Specify recurse=True to get children recursively.
        Layers are always given in the user-visible order.
        '''
        if parent is None:
            cond = 'is null'
        elif isinstance(parent, Layer):
            cond = f' = "{layer.uuid}"'
        elif isinstance(parent, str):
            cond = f' = "{parent}"'
        else:
            raise TypeError('ID must be a layer, UUID or None.')

        children = [self._layer(ID) for (ID, ) in self.db.execute(
            "select id from document_layers"
            f" where parent_identifier {cond}"
            " order by index_at_parent asc;",
        ).fetchall()]
        if recurse:
            tree = []
            for child in children:
                tree.append(child)
                tree += self.layers(child._uuid, recurse=True)
            return tree
        else:
            return children

    def layer_with_name(self, name):
        '''Get the first layer found with the given name.'''
        layers = [
            l for l in self.layers(recurse=True)
            if l.name == name
        ]
        return layers[0]

    def close(self):
        self.db.close()

    def __enter__(self):
        self.db.execute('PRAGMA journal_mode=DELETE')
        self.db.execute('begin exclusive')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.execute('commit')
        return True

    def __del__(self):
        self.close()
