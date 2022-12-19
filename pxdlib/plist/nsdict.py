from types import MappingProxyType

from .nsobject import NSObject

class NSDict(NSObject):
    '''
    Auto-dereferencing NSDictionary for PlistFile.
    By default, repr() shows UIDs; str() dereferences them.
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
        return __o in NSDict.keys(self)

    def keys(self):
        return NSDict._deref(self,
            NSObject.__getitem__(self, 'NS.keys'))
    
    def values(self):
        return NSDict._deref(self,
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
    