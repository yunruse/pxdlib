from math import pi
from uuid import uuid1

from .helpers import dicts, reversegetattr
from .structure import RGBA, Gradient
from .enums import (
    FillType, BlendMode, StrokeType, StrokePosition
)

_STYLE_TAGS = {
    'E': 'enabled',
    'o': 'opacity',
    'B': 'blendMode',
    'c': 'color',
    'fT': 'fillType',
    'g': 'gradient',
    '_gPos': 'gradientPosition',
    'sT': 'strokeType',
    'sP': 'strokePosition',
    'sW': 'strokeWidth',
    'b': 'blur',
    'd': 'distance',
    'a': 'angle',
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
        _dict = dict(self._defaults)
        _dict.update(kwargs)
        if 'gSP' in _dict:
            _dict['_gPos'] = (
                _dict.pop('gSP'), _dict.pop('gEP')
            )
        for i in _dict:
            if i not in self._defaults:
                raise ValueError(f'Unknown property {i}.')

        self._dict = _dict

        if self._dict.get('id') is None:
            self._dict['id'] = uuid1()

    def __repr__(self):
        args = ', '.join([
            f'{_STYLE_TAGS[k]}={getattr(self, _STYLE_TAGS[k])}'
            for k, v in self._dict.items()
            if k in _STYLE_TAGS
            and self._dict[k] != self._defaults[k]
        ])
        return f'{type(self).__name__}({args})'

    @classmethod
    def _from_layer(cls, data):
        '''Internal binding'''
        return cls(**data)

    def _to_layer(self):
        '''Internal binding'''
        data = self._dict
        if '_gPos' in data:
            data['gSP'], data['gEP'] = data.pop('_gPos')
        return data

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

    @property
    def color(self) -> RGBA:
        return RGBA._from_data(self._dict['c'])

    @color.setter
    def color(self, val: RGBA):
        if not isinstance(val, RGBA):
            val = RGBA(val)
        self._dict['c'] = val._to_data()


class _Blend:
    # Mixin for blend modes
    @property
    def blendMode(self) -> BlendMode:
        '''The blend mode used for the style.'''
        return getattr(BlendMode, self._dict['B'])

    @blendMode.setter
    def blendMode(self, val: BlendMode):
        '''The blend mode used for the style.'''
        val = reversegetattr(BlendMode, val, 'sourceOver')
        val = val.replace('normal', 'sourceOver')
        self._dict['B'] = val


class _Fill:
    # Mixin for gradients
    @property
    def fillType(self) -> FillType:
        return FillType(self._dict['fT'])

    @fillType.setter
    def fillType(self, val: FillType):
        self._dict['fT'] = int(FillType(val))

    @property
    def gradientPosition(self) -> tuple:
        return self._dict['_gPos']

    @gradientPosition.setter
    def gradientPosition(self, val: tuple):
        (x0, y0), (x1, y1) = val
        self._dict['_gPos'] = val

    @property
    def gradient(self) -> Gradient:
        return Gradient._from_data(self._dict['g'])

    @gradient.setter
    def gradient(self, val: Gradient):
        self._dict['g'] = val._to_data()


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
    'c': RGBA()._to_data(),
    '_gPos': ([0, 0.5], [1, 0.5]),
    'B': 'sourceOver',
}

_FILL_DEFAULT = {
    'fT': 0,
}
_SHADOW_DEFAULT = {
    'o': 0.5,
    'b': 5,
    'd': 2,
}


class Fill(Style, _Fill, _Blend):
    _defaults = dicts(
        _STYLE_DEFAULT, _FILL_DEFAULT, {
            'c': [1, {'m': 2, 'c': [0, 0.635, 1, 1], 'csr': 0}],
            'g': [1, {'m': [0.5], 'csr': 0, 's': [[1, [[0.2823529411764706, 0.6274509803921569, 0.9725490196078431, 1], 0]], [1, [[0.2823529411764706, 0.6274509803921569, 0.9725490196078431, 0], 1]]], 't': 0}]
        }
    )
    _tag = 'f'


class Stroke(Style, _Fill, _Blend):
    _defaults = dicts(
        _STYLE_DEFAULT, _FILL_DEFAULT, {
            'sT': 0,
            'sP': 1,
            'sW': 3,
            'g': [1, {'m': [0.5], 'csr': 0, 's': [[1, [[0, 0, 0, 1], 0]], [1, [[1, 1, 1, 1], 1]]], 't': 0}],
        }
    )
    _tag = 's'

    @property
    def strokeType(self) -> StrokeType:
        return StrokeType(self._dict['sT'])

    @strokeType.setter
    def strokeType(self, val: StrokeType):
        self._dict['sT'] = int(StrokeType(val))

    @property
    def strokePosition(self) -> StrokePosition:
        return StrokePosition(self._dict['sP'])

    @strokePosition.setter
    def strokePosition(self, val: StrokePosition):
        self._dict['sP'] = int(StrokePosition(val))

    @property
    def strokeWidth(self) -> float:
        return self._dict['sW']

    @strokeWidth.setter
    def strokeWidth(self, val: float):
        self._dict['sW'] = float(val)


class Shadow(Style, _Shadow, _Blend):
    _defaults = dicts(
        _STYLE_DEFAULT, _SHADOW_DEFAULT, {
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
