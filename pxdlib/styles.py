from math import pi

from .enums import BlendMode


class Style(dict):
    '''
    A style applied to a layer.

    Modifying a Style will not have a direct effect on a layer.
    '''
    _tag = None

    def __init__(self, data):
        # TODO: non-dict format
        dict.__init__(self, data)

    def __repr__(self):
        return f'{type(self).__name__}({dict.__repr__(self)})'

    @classmethod
    def _from_layer(cls, data):
        return cls(data)


class _StyleWithBlend:
    # Mixin for blend modes
    @property
    def blendMode(self):
        '''The blend mode used for the style.'''
        return getattr(BlendMode, self['B'])


'''
- `b` is the blur (in pixels);
- `d` is the distance (in pixels);
- `a` is the angle used for distance (in radians, from 0 through 2pi);
'''


class _Shadow:
    # Mixin for shadow stuff
    @property
    def blur(self):
        '''The blur intensity of the shadow, in pixels.'''
        return self['b']

    @property
    def distance(self):
        '''The distance of the shadow from its object, in pixels.'''
        return self['d']

    @property
    def angle(self):
        '''The angle of the shadow's distance in degrees clockwise from north.'''
        angle_ccw_E = self['a'] * 180 / pi
        return (90 - angle_ccw_E) % 360


class Fill(Style, _StyleWithBlend):
    _tag = 'f'


class Stroke(Style, _StyleWithBlend):
    _tag = 's'


class Shadow(Style, _Shadow, _StyleWithBlend):
    _tag = 'S'


class InnerShadow(Style, _Shadow):
    _tag = 'i'


_STYLES = {c._tag: c for c in (Fill, Stroke, Shadow, InnerShadow)}
