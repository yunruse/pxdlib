'''
NSBaseObject, NSObject, PlistDerefList, NSDict and NSArray wrappers.

By default, these items will dereference all UIDs in str() but may truncate some in repr() to avoid chaos.
'''

from functools import total_ordering, wraps
from plistlib import UID
from typing import Any, TYPE_CHECKING, Type
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
        if NSObject.__contains__(self, key):
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
        return NSDictionary_items(self)

class NSDictionary_items:
    '''dict_items for NSDictionary'''
    def __init__(self, dict):
        self.mapping = MappingProxyType(dict)
    
    def __repr__(self):
        return 'NSDict_items({})'.format(repr(list(self)))
    
    def __iter__(self):
        for k, v in zip(self.mapping.keys(), self.mapping.values()):
            yield k, v


def add_str_and_bytes_methods(cls):
    '''
    Add methods from `str` and `bytes`,
    passing directly through to `self.value`.
    (An AttributeError is raised if self.value is not the right type.)
    '''
    str_methods = set(dir(str))
    bytes_methods = set(dir(bytes))

    shared_methods = bytes_methods & str_methods
    shared_methods -= {
        '__sizeof__', '__class__', '__subclasshook__',
        '__init_subclass__', '__init__', '__new__',
        '__getitem__',      '__setitem__', '__delitem__',
        '__getattribute__', '__setattr__', '__delattr__',
        '__reduce__', '__reduce_ex__', '__getnewargs__', '__getstate__'
    }

    def wrap_shared(key):
        @wraps(getattr(str, key))
        def wrapped(self, *args, **kwargs):
            return getattr(self.value, key)(*args, **kwargs)
        return wrapped

    for k in shared_methods:
        if not hasattr(cls, k):
            setattr(cls, k, wrap_shared(k))
    
    def wrap_typed(key, T):
        @wraps(getattr(T, key))
        def wrapped(self, *args, **kwargs):
            if isinstance(self.value, T):
                return getattr(self.value, key)(*args, **kwargs)
            else:
                raise AttributeError(
                    '{} cannot use method {} (requires {}, not {})'.format(
                        self.classname, k, T.__name__, self.type.__name__))
        return wrapped
    
    for T, type_methods in (
        (str, str_methods - bytes_methods),
        (bytes, bytes_methods - str_methods),
    ):
        for k in type_methods:
            if not hasattr(cls, k):
                setattr(cls, k, wrap_typed(k, T))

    return cls

@add_str_and_bytes_methods
@total_ordering
class NSStringOrData(NSObject):
    '''
    Object that represents str- or bytes-like objects:
    NSString, NSMutableString, NSData, NSMutableData.

    .value is the value (which can be set iff mutable);
    .type is its type;
    .mutable is if it is mutable.
    The rest are common str- and bytes methods.
    '''

    NSCLASS_PROPERTIES: dict[str, tuple[Type, bool]] = {
        'NSString': (str, False),
        'NSMutableString': (str, True),
        'NSData': (bytes, False),
        'NSMutableData': (bytes, True),
    }
    _TYPE_PROPERTIES = {
        str: 'NS.string',
        bytes: 'NS.data'
    }

    classname: str
    value: str | bytes
    
    def __init__(self, value, parent: "PlistFile"):
        NSObject.__init__(self, value, parent)
        self.classname = classname(self)
        self._type_property = self._TYPE_PROPERTIES[self.type]

    @property
    def type(self) -> Type:
        return self.NSCLASS_PROPERTIES[self.classname][0]

    @property
    def mutable(self) -> bool:
        return self.NSCLASS_PROPERTIES[self.classname][1]

    @property
    def value(self) -> bytes | str:
        return self[self._type_property]
    
    @value.setter
    def value(self, new_value: bytes | str):
        if not self.mutable:
            raise AttributeError("Cannot change value of a {}".format(
                self.classname))
        
        if not isinstance(new_value, self.type):
            raise AttributeError("{} can only take type {}".format(
                self.classname, self.type.__name__))
        
        self[self._type_property] = new_value
        # TODO: propagate...? maybe?
    
    def __repr__(self):
        return '<{}: {!r}>'.format(
            self.classname, self.value
    )

    def __str__(self): return str(self.value)
    def __len__(self): return len(self.value)
