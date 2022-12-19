'''
NSBaseObject, NSObject, PlistDerefList, NSDict and NSArray wrappers.

By default, these items will dereference all UIDs in str() but may truncate some in repr() to avoid chaos.
'''

from plistlib import UID
from typing import Any, TYPE_CHECKING
from types import MappingProxyType

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
        if __name in dict.keys(self):
            return self[__name]
        return object.__getattribute__(self, __name)


class NSArray(NSObject):
    '''
    Auto-dereferencing NSArray for PlistFile.
    '''
    
    def __repr__(self):
        return '<NSArray: [{}]>'.format(', '.join(
            self._repr_child(i) for i in self
        ))
    
    def __iter__(self):
        for k in self['NS.objects']:
            yield k
    
    def __getitem__(self, index: int):
        if isinstance(index, int):
            return self['NS.objects'][index]
        else:
            return NSObject.__getitem__(self, index)
    

class NSDictionary(NSObject):
    '''
    Auto-dereferencing NSDict for PlistFile.
    '''
    
    def __repr__(self):
        return '<NSDict: {}>'.format(', '.join(
            f'{self._deref(k)}: {self._repr_child(v)}' for k, v in self.items()
        ))
    
    def __getitem__(self, key: str):
        index = self.keys().index(key)
        return self.values()[index]

    # TODO: All code below should be changed to use mappingproxy

    # These unorthodox class.func(self) calls
    # are to avoid infinite recursion in __getattribute__

    def __contains__(self, __o: object) -> bool:
        return __o in NSDictionary.keys(self)

    def keys(self):
        return NSDictionary._deref(self,
            NSObject.__getitem__(self, 'NS.keys'))
    
    def values(self):
        return NSDictionary._deref(self,
            NSObject.__getitem__(self, 'NS.objects'))
    
    def items(self):
        return NSDict_items(self)

class NSDict_items:
    def __init__(self, dict):
        self.mapping = MappingProxyType(dict)
    
    def __repr__(self):
        return 'NSDict_items({})'.format(repr(list(self)))
    
    def __iter__(self):
        for k, v in zip(self.mapping.keys(), self.mapping.values()):
            yield k, v
    