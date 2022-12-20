from .plist import NSDictionary
from .color import Color

TEXTKIT_PREFIX = 'com.pixelmatorteam.textkit.attribute.'

class TextStyle:
    def __init__(self, style_dict: NSDictionary):
        self._info = style_dict
    
    def _get(self, key, default=None):
        return self._info.get(TEXTKIT_PREFIX + key, default)
    
    @property
    def _font(self):
        return self._get('font')['NSFontDescriptorAttributes']
    
    @property
    def font_family(self):
        return self._font['NSFontFamilyAttribute']
    
    @property
    def font_face(self):
        return self._font['NSFontFaceAttribute']
    
    @property
    def is_strikethrough(self):
        return bool(self._get('strikethrough', 0))
    
    @property
    def is_underline(self):
        return bool(self._get('underline', 0))
    
    @property
    def color(self):
        desc: bytes = self._get('color').NSComponents
        color = [float(x) for x in desc.decode().split()]
        return Color.from_rgb(*color[:3])
    
    @color.setter
    def color(self, color: Color):
        raise NotImplementedError('Cannot set color')
        if not isinstance(color, Color):
            raise TypeError('Can only set color to a Color')
        self._get('color').NSComponents = '{} {} {} 1'.format(
            color.r, color.g, color.b).encode()

    def _repr_info(self):
        yield self.font_family
        yield self.font_face
        yield str(self.color)

    def __repr__(self):
        info = list(self._repr_info())
        return '<TextStyle: {}>'.format(
            ', '.join(info))