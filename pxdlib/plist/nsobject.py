from plistlib import UID
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .plistfile import PlistFile

def classname(obj: dict):
    return obj.get('$class', {}).get('$classname', None)

def classisinstance(obj: dict, key: str):
    return key in obj.get('$class', {}).get('$classes', [])

class NSBaseObject:
    def _deref(self, value):
        return self._parent._deref(value)
    
    def _repr_child(self, value):
        if isinstance(value, UID):
            deref = self._deref(value)
            if isinstance(deref, NSBaseObject):
                return '<{}>'.format(classname(deref))
            else:
                return repr(deref)
        
        return repr(value)
    
    def __init__(self, value, parent: "PlistFile"):
        self._parent = parent
        self._super_type.__init__(self, value)
    
    def __getitem__(self, key: int) -> Any:
        return self._deref(self._super_type.__getitem__(self, key))


class PlistDerefList(NSBaseObject, list):
    '''
    Auto-dereferencing list for PlistFile.
    repr() may show UIDs for complex objects, but str() dereferences them.
    '''
    _super_type = list
    
    def __str__(self):
        return '[{}]'.format(', '.join([
            str(self._deref(v)) for v in self
        ]))
    
    def __repr__(self):
        return '<PlistDerefList: [{}]>'.format(', '.join(
            self._repr_child(v) for v in self
        ))
    
    def __iter__(self):
        for i in list.__iter__(self):
            yield self._deref(i)

class NSObject(NSBaseObject, dict):
    '''
    Auto-dereferencing object (aka dict) for PlistFile.
    repr() may show UIDs for complex objects, but str() dereferences them.
    '''
    _super_type = dict
    
    def __init__(self, value, parent: "PlistFile"):
        self._parent = parent
        dict.__init__(self, value)
    
    def __str__(self):
        return '{{{}}}'.format(', '.join([
            f'{k}: {self._parent._deref(v)}' for k, v in self.items()
        ]))
    
    def __repr__(self):
        keys = list(self.keys())
        if '$class' in keys:
            keys.remove('$class')
        return '<{} with keys {}>'.format(
            classname(self) or 'dict', ', '.join(keys)
        )
    
    def get(self, key, default=None):
        if key in self:
            return self[key]
        else:
            return default
    
    def __getattribute__(self, __name: str) -> Any:
        if __name in self:
            return self[__name]
        return object.__getattribute__(self, __name)
