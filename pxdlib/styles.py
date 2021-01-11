from math import pi
from uuid import uuid1

from .enums import BlendMode



class Style:
    '''
    A style applied to a layer.

    Modifying a Style will not have a direct effect on a layer.
    '''
    _tag = None

    def __init__(self, **kwargs):
        if type(self) == Style:
            raise TypeError(
                'Cannot directly instantiate a Style. Try Fill, Stroke, Shadow or InnerShadow')
        _dict = dict()
        _dict.update(self._defaults)
        _dict.update(kwargs)
        self._dict = _dict

        if self._dict.get('id') is None:
            self._dict['id'] = uuid1()

    def __repr__(self):
        return f'{type(self).__name__}({repr(self._dict)})'

    @classmethod
    def _from_layer(cls, data):
        '''Internal binding for layer.styles'''
        return cls(**data)

    @property
    def enabled(self) -> bool:
        return bool(self._dict['E'])

    @enabled.setter
    def enabled(self, val: bool):
        self._dict['E'] = int(bool(val))

    @property
    def opacity(self) -> float:
        return self._dict['o']

    @opacity.setter
    def opacity(self, val: float):
        self._dict['o'] = float(val)


class _StyleWithBlend:
    # Mixin for blend modes
    @property
    def blendMode(self):
        '''The blend mode used for the style.'''
        return getattr(BlendMode, self._dict['B'])


'''
- `b` is the blur (in pixels);
- `d` is the distance (in pixels);
- `a` is the angle used for distance (in radians, from 0 through 2pi);
'''


class _Shadow:
    # Mixin for shadow stuff
    @property
    def blur(self) -> float:
        '''The blur intensity of the shadow, in pixels.'''
        return self._dict['b']

    @property
    def distance(self) -> float:
        '''The distance of the shadow from its object, in pixels.'''
        return self._dict['d']

    @property
    def angle(self):
        '''The angle of the shadow's distance in degrees clockwise from north.'''
        angle_ccw_E = self._dict['a'] * 180 / pi
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
