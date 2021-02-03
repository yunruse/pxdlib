'''
Color and Gradient structures for interacting with PXDFiles.
'''

import colorsys

from .structure import verb
from .enums import GradientType
from .helpers import num, hexbyte


class Color:
    '''
    A color.

    May be instantiated in [0, 255]-space, or in
    [0, 1]-space for various formats defined in colorsys.
    '''

    def __init__(self, r=0, g=0, b=0, a=255):
        '''
        Accepts a hex string, or RGBA values in [0, 255]-space.
        '''
        if isinstance(r, Color):
            r, g, b, a = r.r, r.g, r.b, r.a
        elif isinstance(r, (tuple, list)):
            if len(r) == 3:
                r, g, b = r
            elif len(r) == 4:
                r, g, b, a = r
            else:
                raise ValueError('Iterable must be length 3 or 4.')
        elif isinstance(r, str):
            string = r
            if string.startswith('#'):
                string = string[1:]
            if not len(string) in (6, 8):
                raise ValueError(
                    'String colors must be #RRGGBB or #RRGGBBAA.'
                )
            r = int(string[0:2], base=16)
            g = int(string[2:4], base=16)
            b = int(string[4:6], base=16)
            if len(string) == 8:
                a = int(string[6:8], base=16)
        self.r = num(r)
        self.g = num(g)
        self.b = num(b)
        self.a = num(a)

    @classmethod
    def from_rgb(cls, r, g, b, a=1):
        return cls(r*255, g*255, b*255, a*255)

    @classmethod
    def from_hsv(cls, h, s, v, a=1):
        return cls.from_rgb(*colorsys.hsv_to_rgb(h, s, v), a)

    @classmethod
    def from_hls(cls, h, l, s, a=1):
        return cls.from_rgb(*colorsys.hls_to_rgb(h, l, s), a)

    @classmethod
    def from_yiq(cls, y, i, q, a=1):
        return cls.from_rgb(*colorsys.yiq_to_rgb(y, i, q), a)

    def __iter__(self):
        tup = self.r, self.g, self.b, self.a
        return iter(tup)

    def __str__(self):
        val = hexbyte(self.r) + hexbyte(self.g) + hexbyte(self.b)
        if self.a != 255:
            val += hexbyte(self.a)
        return '#' + val

    def __repr__(self):
        return f"Color('{str(self)}')"

    @classmethod
    def _from_data(cls, data):
        data = verb(data)
        assert data['m'] == 2
        assert data['csr'] == 0
        r, g, b, a = data['c']
        return cls(r*255, g*255, b*255, a*255)

    def _to_data(self):
        r, g, b, a = list(self)
        return [1, {
            'm': 2, 'csr': 0,
            'c': [r/255, g/255, b/255, a/255]
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

    def __init__(self, *colors, midpoints=None, kind=GradientType.linear):
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
        assert data['csr'] == 0
        colors = [verb(i) for i in data['s']]
        return cls([
            (Color(r*255, g*255, b*255, a*255), x)
            for (r, g, b, a), x in colors
        ], midpoints=data['m'], kind=data['t'])

    def _to_data(self):
        data = {'csr': 0}
        data['m'] = list(self.midpoints)
        data['s'] = [
            [1, [[c.r/255, c.g/255, c.g/255, c.a/255], x]]
            for c, x in self.colors
        ]
        data['t'] = int(self.kind)
        return [1, data]
