from .plist import NSDictionary

TEXTKIT_PREFIX = 'com.pixelmatorteam.textkit.attribute.'

class TextStyle:
    def __init__(self, style_dict: NSDictionary):
        self._info = style_dict
    
    @property
    def _font(self):
        return self._info[TEXTKIT_PREFIX + 'font']['NSFontDescriptorAttributes']
    
    @property
    def font_family(self):
        return self._font['NSFontFamilyAttribute']
    
    @property
    def font_face(self):
        return self._font['NSFontFaceAttribute']

    def _repr_info(self):
        yield self.font_family
        yield self.font_face

    def __repr__(self):
        info = list(self._repr_info())
        return '<TextStyle: {}>'.format(
            ', '.join(info))