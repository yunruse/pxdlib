'''
Database wrapper which exposes a `with` block interface for editing.

This file, originally by Mia Dobson,
is public domain and free of any outside license.
'''

from io import UnsupportedOperation
import sqlite3
from typing import Optional

class DatabaseModeError(UnsupportedOperation):
    pass

class Database:
    '''
    Database wrapper which exposes a `with` block interface for editing.
    '''
    _db: sqlite3.Connection

    def __init__(self, path):
        self._db = sqlite3.connect(path)
        self.__can_write = False
    
    @property
    def can_write(self):
        return self.__can_write

    def open(self) -> None:
        '''
        Starts a transaction to modify the document.

        Changes will only be made on `close()`.
        '''
        if self.__can_write:
            return
        self._db.execute('PRAGMA journal_mode=DELETE')
        self._db.execute('begin exclusive')
        self.__can_write = True

    def close(self) -> None:
        '''
        Closes a transaction and commits any changes made.
        '''
        if not self.__can_write:
            return
        self._db.execute('commit')
        self.__can_write = False

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _assert(self, *, write: Optional[bool] = None):
        '''Assert database is in correct mode.'''
        if write is not None:
            if write is True and self.can_write is False:
                raise DatabaseModeError(
                    'Database must be open for writing. Please use a `with` block or .open()')
            if write is False and self.can_write is True:
                raise DatabaseModeError(
                    'Database must not be open for writing. Please use a `with` block or .close()')
        
        if hasattr(self, '_db'): return
        raise DatabaseModeError('Database not readable.')
