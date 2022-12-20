from plistlib import UID
from typing import Any

from .nsobject import (
    NSObject,   
    PlistDerefList,
    classisinstance,
)
from .nsprimitives import NSDictionary, NSArray, NSStringOrData

class PlistFile(NSObject):
    '''
    .plist as loaded from Pixelmator with $objects.
    
    Currently read-only, yay dereferencing!
    '''

    # TODO: Make writeable!
    # TODO: Add test methods???

    def _object(self, id: UID):
        return self._tree['$objects'][id]

    def __init__(self, object, **kwargs):
        self._tree = object

        root_id = dict.__getitem__(object, '$top')['root']
        root = self._object(root_id)
        NSObject.__init__(self, root, self)

        # root_id is usually 1
    
    DEREF_MAPS: dict[str, type] = {
        'NSDictionary': NSDictionary,
        'NSArray': NSArray,
        'NSString': NSStringOrData,
        'NSData': NSStringOrData,
    }

    def _deref(self, value) -> NSObject | Any:
        if isinstance(value, UID):
            value = self._object(value)

        if isinstance(value, list):
            return PlistDerefList(value, self)
        if isinstance(value, dict):
            value = NSObject(value, self)
            for NSClass, cls in self.DEREF_MAPS.items():
                if classisinstance(value, NSClass):
                    return cls(value, self)

        return value