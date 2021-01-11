from math import pi
from uuid import uuid1

from .helpers import dicts
from .enums import BlendMode, StrokeType, StrokePosition

_STYLE_TAGS = {
    'E': 'enabled',
    'o': 'opacity',
    'B': 'blendMode',
    'b': 'blur',
    'd': 'distance',
    'a': 'angle',
    'gEP': 'gradientStart',
    'gSP': 'gradientEnd',
    'sT': 'strokeType',
    'sP': 'strokePosition',
    'sW': 'strokeWidth',
}


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
        args = ', '.join([
            f'{_STYLE_TAGS[k]}={getattr(self, _STYLE_TAGS[k])}'
            for k, v in self._dict.items()
            if self._dict[k] != self._defaults[k]
            and k in _STYLE_TAGS
        ])
        return f'{type(self).__name__}({args})'

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


class _Blend:
    # Mixin for blend modes
    @property
    def blendMode(self):
        '''The blend mode used for the style.'''
        return getattr(BlendMode, self._dict['B'])


class _Fill:
    # Mixin for gradients
    pass


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
    def angle(self) -> float:
        '''The angle of the shadow's distance in degrees clockwise from north.'''
        angle_ccw_E = self._dict['a'] * 180 / pi
        return (90 - angle_ccw_E) % 360


_STYLE_DEFAULT = {
    'id': None,
    'V': 1,
    'C': 1,
    'E': 1,
    'o': 1,
    'g': [1, {'m': [0.5], 'csr': 0, 's': [[1, [[0.20392156862745098, 0.47058823529411764, 0.9647058823529412, 1], 0]], [1, [[0.3254901960784314, 0.7137254901960784, 0.9764705882352941, 1], 1]]], 't': 0}],
    'c': [1, {'m': 2, 'c': [0, 0.635, 1, 1], 'csr': 0}],
    'gSP': [0, 0.5],
    'gEP': [1, 0.5],
}

_BLEND_DEFAULT = {
    'B': 'sourceOver',
}
_FILL_DEFAULT = {
    'fT': 0,
}
_SHADOW_DEFAULT = {
    'b': 5,
    'd': 2,
}


class Fill(Style, _Fill, _Blend):
    _defaults = dicts(
        _STYLE_DEFAULT, _BLEND_DEFAULT, _FILL_DEFAULT
    )
    _tag = 'f'


class Stroke(Style, _Fill, _Blend):
    _defaults = dicts(
        _STYLE_DEFAULT, _BLEND_DEFAULT, _FILL_DEFAULT, {
            'sT': 0,
            'sP': 1,
            'sW': 3,
        }
    )
    _tag = 's'

    @property
    def strokeType(self) -> StrokeType:
        return StrokeType(self._dict['sT'])

    @strokeType.setter
    def strokeType(self, val: StrokeType):
        assert val in [0, 1, 2]
        self._dict['sT'] = int(val)

    @property
    def strokePosition(self) -> StrokePosition:
        return StrokePosition(self._dict['sP'])

    @strokePosition.setter
    def strokePosition(self, val: StrokePosition):
        assert val in [0, 1, 2]
        self._dict['sP'] = int(val)

    @property
    def strokeWidth(self) -> float:
        return self._dict['sW']

    @strokeWidth.setter
    def strokeWidth(self, val: float):
        self._dict['sW'] = float(val)


class Shadow(Style, _Shadow, _Blend):
    _defaults = dicts(
        _STYLE_DEFAULT, _BLEND_DEFAULT, _SHADOW_DEFAULT, {
            'a': pi * 1.5,
        }
    )
    _tag = 'S'


class InnerShadow(Style, _Shadow):
    _defaults = dicts(
        _STYLE_DEFAULT, _SHADOW_DEFAULT, {
            'a': pi * 0.5,
        }
    )
    _tag = 'i'


_STYLES = {c._tag: c for c in (Fill, Stroke, Shadow, InnerShadow)}
