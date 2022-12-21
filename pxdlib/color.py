'''
Color and Gradient structures for interacting with PXDFiles.
'''

import colorsys
from typing import Any, Iterable

from .structure import verb
from .enums import GradientType
from .helpers import num, hexbyte, add_tuple_shortcuts, add_shortcuts

Number = int | float
ColorInput = str | Number | tuple

@add_tuple_shortcuts('hsv', ('h', 'sv', 'v'))
@add_tuple_shortcuts('hls', ('h', 'l', 'sl'))
@add_tuple_shortcuts('yiq', ('y', 'i', 'q'))
@add_tuple_shortcuts('rgb', ('r', 'g', 'b'))
@add_shortcuts({
    'a': ('alpha', ),
    'h': ('hue', ),
    'v': ('val', 'value'),
    'l': ('lum', 'lumin', 'luminosity'),
    'r': ('red', ),
    'g': ('green', ),
    'b': ('blue', ),
})
class Color:
    '''
    A color.

    May be instantiated in [0, 255]-space, or in
    [0, 1]-space for various formats defined in colorsys.
    '''
    __slots__ = ('R', 'G', 'B', 'A')

    def __hash__(self):
        return hash(str(self))

    def __init__(
        self,
        R: ColorInput = 0,
        G: Number = 0,
        B: Number = 0,
        A: Number = 255
    ):
        '''
        Accepts a hex string, or RGBA values in [0, 255]-space.
        '''
        if isinstance(R, Color):
            R, G, B, A = R.R, R.G, R.B, R.a
        elif isinstance(R, (tuple, list)):
            if len(R) == 3:
                R, G, B = R
            elif len(R) == 4:
                R, G, B, A = R
            else:
                raise ValueError('Iterable must be length 3 or 4.')
        elif isinstance(R, str):
            string = R
            if string.startswith('#'):
                string = string[1:]
            if not len(string) in (6, 8):
                raise ValueError(
                    'String colors must be #RRGGBB or #RRGGBBAA.'
                )
            R = int(string[0:2], base=16)
            G = int(string[2:4], base=16)
            B = int(string[4:6], base=16)
            if len(string) == 8:
                A = int(string[6:8], base=16)
        self.R = num(R)
        self.G = num(G)
        self.B = num(B)
        self.A = num(A)

    @classmethod
    def from_rgb(cls, r: Number, g: Number, b: Number, a: Number = 1):
        return cls(r*255, g*255, b*255, a*255)

    @property
    def a(self):
        return self.A / 255

    @property
    def rgb(self):
        return (self.R/255, self.G/255, self.B/255)

    @rgb.setter
    def rgb(self, val):
        r, g, b = val
        self.R = r * 255
        self.G = g * 255
        self.B = g * 255

    @classmethod
    def from_hsv(cls, h, s, v, a=1):
        return cls.from_rgb(*colorsys.hsv_to_rgb(h, s, v), a)

    @property
    def hsv(self):
        return colorsys.rgb_to_hsv(*self.rgb)

    @hsv.setter
    def hsv(self, val):
        self.rgb = colorsys.hsv_to_rgb(*val)

    @classmethod
    def from_hls(cls, h, l, s, a=1):
        return cls.from_rgb(*colorsys.hls_to_rgb(h, l, s), a)

    @property
    def hls(self):
        return colorsys.rgb_to_hls(*self.rgb)

    @hls.setter
    def hls(self, val):
        self.rgb = colorsys.hls_to_rgb(*val)

    @classmethod
    def from_yiq(cls, y, i, q, a=1):
        return cls.from_rgb(*colorsys.yiq_to_rgb(y, i, q), a)

    @property
    def yiq(self):
        return colorsys.rgb_to_yiq(*self.rgb)

    @yiq.setter
    def yiq(self, val):
        self.rgb = colorsys.yiq_to_rgb(*val)

    def __iter__(self):
        return iter((self.R, self.G, self.B, self.a))

    def __str__(self):
        val = hexbyte(self.R) + hexbyte(self.G) + hexbyte(self.B)
        if self.A != 255:
            val += hexbyte(self.A)
        return '#' + val

    def __repr__(self):
        return f"Color('{str(self)}')"

    @classmethod
    def _from_data(cls, data):
        data = verb(data)
        assert data['m'] == 2
        # assert data['csr'] == 0
        return cls.from_rgb(*data['c'])

    def _to_data(self):
        return [1, {
            'm': 2, 'csr': 0,
            'c': self.rgb
        }]

    def __eq__(self, other):
        return all([
            round(a[0]) == round(a[1])
            for a in zip(tuple(self), tuple(other))
        ])


class Gradient:
    '''
    Gradient of two or more colours.

    Contains a list of colors, or a list of (col, x)
    for position x in the range [0, 1].
    Midpoints for the gradient interpolation
    can be provided but default to the position midpoint.
    '''

    _default_cols = ['48a0f8' '48a0f800']

    def __init__(
        self,
        *colors: Iterable[tuple[ColorInput, float]],
        midpoints = None,
        kind = GradientType.linear
    ):
        if len(colors) == 1 and isinstance(colors[0], (list, tuple)):
            colors = colors[0]
        self.kind = GradientType(kind)

        colors = colors or self._default_cols
        pos_provided = isinstance(colors[0], tuple)

        if pos_provided:
            self.colors = []
            x0 = -1
            for c, x in colors:
                assert x0 < x
                x0 = x
                self.colors.append((Color(c), x))
        else:
            # no positions, so at equal steps
            self.colors = [
                (Color(c), i/(len(colors)-1))
                for i, c in enumerate(colors)
            ]

        if midpoints is None:
            midpoints = []
            for i in range(len(self.colors) - 1):
                c1, x1 = self.colors[i]
                c2, x2 = self.colors[i+1]
                midpoints.append((x1 + x2)/2)
        else:
            M = len(midpoints)
            C = len(self.colors)
            if M != C - 1:
                raise ValueError(
                    f'Need {C-1} midpoints, got {M}.'
                )
        self.midpoints = midpoints

    def is_positions_default(self):
        N = len(self.colors) - 1
        for i, (c, x) in enumerate(self.colors):
            x_apparent = i / N
            if x != x_apparent:
                return False
        return True

    def is_midpoints_default(self):
        for i in range(len(self.colors) - 1):
            c1, x1 = self.colors[i]
            c2, x2 = self.colors[i+1]
            m_apparent = (x1 + x2)/2
            m = self.midpoints[i]
            if m != m_apparent:
                return False
        return True

    def __repr__(self):
        vals = []
        if self.colors != self._default_cols:
            col_only = self.is_positions_default()
            vals.append(', '.join([
                repr(str(c) if col_only else (str(c), x))
                for c, x in self.colors]))

        if not self.is_midpoints_default():
            vals.append('midpoints=' + str(self.midpoints))

        if self.kind != 0:
            vals.append('kind=' + str(self.kind))

        return f"{type(self).__name__}({', '.join(vals)})"

    @classmethod
    def _from_data(cls, data):
        data = verb(data)
        # assert data['csr'] == 0
        colors = [verb(i) for i in data['s']]
        return cls([
            (Color.from_rgb(*c), x)
            for c, x in colors
        ], midpoints=data['m'], kind=data['t'])

    def _to_data(self):
        data: dict[str, Any] = {'csr': 0}
        data['m'] = list(self.midpoints)
        data['s'] = [
            [1, [c.rgb, x]]
            for c, x in self.colors
        ]
        data['t'] = int(self.kind)
        return [1, data]
