from plistlib import UID

from .nsobject import (
    NSObject,
    NSDictionary,
    NSArray,
    PlistDerefList,
    classisinstance,
)

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

    def _deref(self, value):
        if isinstance(value, UID):
            value = self._object(value)

        if isinstance(value, list):
            return PlistDerefList(value, self)
        if isinstance(value, dict):
            value = NSObject(value, self)
            if classisinstance(value, 'NSDictionary'):
                return NSDictionary(value, self)
            if classisinstance(value, 'NSArray'):
                return NSArray(value, self)
            
        return value