'''
PXDFile class, handling most database access.
'''

from pathlib import Path
import shutil
import sqlite3
from collections import namedtuple
from tempfile import mkdtemp
from zipfile import is_zipfile, ZipFile

from .helpers import add_tuple_shortcuts
from .errors import ModeError

from .layer import _LAYER_TYPES, Layer
from .structure import blob, make_blob

guides = namedtuple('guides', ('horizontal', 'vertical'))


@add_tuple_shortcuts('size', ('width', 'height'))
class PXDFile:
    path: Path  # The path the PXD file or folder is saved at.
    _edit_dir: Path  # The path the PXD folder is editable at.

    _compressed: bool  # True iff the original PXD is a .zip file.

    _open: bool  # True iff open for editing
    _db = sqlite3.Connection  # Always held open for reading
    _layer_cache = dict
    _meta = dict
    _info = dict

    def __repr__(self):
        return f"PXDFile({repr(str(self.path))})"

    def __init__(self, path):
        '''
        A PXD (Pixelmator Pro) file.
        '''

        self.path = Path(path)
        self._edit_dir = self.path
        self._compressed = self.path.is_file()

        if self._compressed:
            if not is_zipfile(self.path):
                raise FileNotFoundError("PXD malformed - is neither directory or .zip")
            
            # Work in a temporary directory!
            self._edit_dir = Path(mkdtemp('.pxd'))
            with ZipFile(self.path) as zf:
                zf.extractall(self._edit_dir)

        self._open = False

        self.reload()
    
    def reload(self):
        '''Reload file after any modification.'''
        if self._open:
            raise ModeError('Cannot reload when open. Please use a `with` block or .close()')

        if not self.path.exists():
            raise FileNotFoundError(f'{self.path} does not exist')
        db_path = self._edit_dir / 'metadata.info'
        if not db_path.is_file():
            raise FileNotFoundError(f"{self.path} is not a valid .pxd file")

        self._db = sqlite3.connect(db_path)
        self._layer_cache = {}

        def keyval(table):
            return dict(self._db.execute(
                f"select key, value from {table};"
            ).fetchall())
        self._meta = keyval('document_meta')
        self._info = keyval('document_info')

    def _assert(self, write=False):
        '''Assert file is in correct mode.'''
        if write and (not self.can_write):
            raise ModeError('File not open for writing. Please use a `with` block or .open()')
        
        if hasattr(self, '_db'): return
        raise ModeError('File not readable.')

    # Database management

    @property
    def can_write(self):
        return self._open

    def open(self) -> None:
        '''
        Starts a transaction to modify the document.

        Changes will only be made on `close()`.
        '''
        if self._open:
            return
        self._db.execute('PRAGMA journal_mode=DELETE')
        self._db.execute('begin exclusive')
        self._open = True

    def close(self) -> None:
        '''
        Closes a transaction and commits any changes made.
        '''
        if not self._open:
            return
        self._db.execute('commit')
        if self._compressed:
            self.path.unlink()
            shutil.make_archive(self.path, 'zip', self._edit_dir)
            shutil.move(self.path + '.zip', self.path)
        self._open = False

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        # TODO: PermissionError??? yay...
        # if self._compressed:
        #     self._edit_dir.unlink(True)

        if hasattr(self, '_db'):
            self._db.close()

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

    def _layers(self, parent=None, recurse=False) -> list[Layer]:
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

    @property
    def children(self) -> list[Layer]:
        return self._layers()

    def all_layers(self) -> list[Layer]:
        return self._layers(recurse=True)

    def find(self, name: str, recurse=True):
        '''Get the first child found with the given name.'''
        for l in self._layers(None, recurse):
            if l.name == name:
                return l
    
    # Misc helpers

    def copyto(self, path, overwrite=False):
        '''
        Copy this PXDFile to a path, and return the copy.

        Make sure you pxd.close() so that all changes are saved.
        '''
        self._assert()
        if self.can_write:
            raise ModeError('close file before copying!')

        path = Path(path)
        if path.is_dir():
            if overwrite:
                shutil.rmtree(path)
            else:
                raise FileExistsError(
                    'The .pxd file already exists. Pass overwrite=True, or delete it.')
        shutil.copytree(self.path, path)
        return type(self)(path)

    def _set(self, key, data, is_meta=False):
        self._assert(write=True)
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
    def size(self) -> tuple:
        '''
        The width and height of the document, in pixels.
        '''
        return blob(self._info['size'])

    @size.setter
    def size(self, size: tuple):
        '''
        The width and height of the document, in pixels.
        '''
        w, h = size
        self._set('size', make_blob(b'BDSz', int(w), int(h)))

    @property
    def guides(self):
        '''
        A list of the guides used for visual alignment.

        Given as the list of horizontal guides (0 = left)
        followed by vertical guides (0 = top).
        '''
        data = [blob(b) for b in blob(self._info['guides'])]
        return guides(
            list(sorted(r for _, r, vert in data if not vert)),
            list(sorted(r for _, r, vert in data if vert))
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
