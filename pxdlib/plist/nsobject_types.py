'''
Helper classes for plistfile
that implement various Pixelmator-related types.

At the moment, this is only a reference file;
the class structure is not actually put into use.

Attribute names never contain underlines, but sometimes contain periods.
In this case, the _ represents a . in the attribute name.
'''

from .nsobject import NSObject
from .nsdict import NSDict

class NSString(NSObject):
    NS_string: str

class NSAttributedString(NSObject):
    NSString: NSString
    NSAttributes: NSDict

class NSMutableString(NSString):
    pass
class NSMutableAttributedString(NSAttributedString):
    pass

