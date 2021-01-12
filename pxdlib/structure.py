'''
Basic structures
'''

from struct import Struct

from .helpers import num, hexbyte
from .enums import GradientType

_MAGIC = b'4-tP'
_LENGTH = Struct('<i')


def _bare(fmt: str, mul=None) -> tuple:
    fmt = Struct(fmt)

    def packer(*data) -> bytes:
        if mul is not None:
            data = [x / mul for x in data]
        return fmt.pack(*data)

    def unpacker(data: bytes):
        result = fmt.unpack(data)
        if mul is not None:
            result = [x * mul for x in result]
        if len(result) == 1:
            result = result[0]
        return result
    return packer, unpacker


def string_unpack(data: bytes) -> str:
    length, = _LENGTH.unpack(data[:4])
    return data[4:4+length].decode().replace('\x00', '')


def string_pack(data: str) -> bytes:
    data = data.encode()
    buffer_bytes = -len(data) % 4
    return _LENGTH.pack(len(data)) + data + b'\x00' * buffer_bytes


def array_unpack(data: bytes) -> list:
    length, = _LENGTH.unpack(data[4:8])
    data = data[8:]
    starts = data[:4*length]
    data = data[4*length:]

    blobs = []
    for i in range(length):
        i *= 4
        start, = _LENGTH.unpack(starts[i:i+4])
        end = starts[i+4:i+8]
        if end:
            end, = _LENGTH.unpack(end)
        else:
            end = None
        blob = data[start:end]
        blobs.append(blob)
    return blobs


def array_pack(blobs: list) -> bytes:
    pos = 0
    starts = []
    for blob in blobs:
        starts.append(pos)
        pos += len(blob)

    return (
        _LENGTH.pack(1) + _LENGTH.pack(len(blobs)) +
        b''.join([_LENGTH.pack(i) for i in starts]) +
        b''.join(blobs)
    )


def kind_unpack(data: bytes) -> str:
    return data[::-1].decode()


def kind_pack(data: str) -> bytes:
    return data[::-1].encode()


_FORMATS = {
    b'PTPt': _bare('>dd', mul=2),
    b'PTSz': _bare('>dd', mul=2),
    b'BDSz': _bare('<qq'),
    b'PTFl': _bare('>d'),
    b'Strn': (string_pack, string_unpack),
    b'LOpc': _bare('<H'),
    b'SI16': _bare('<hxx'),
    b'Arry': (array_pack, array_unpack),
    b'Guid': _bare('<hih'),
    b'UI64': _bare('<Q'),
    b'Blnd': (kind_pack, kind_unpack),
}


def blob(blob: bytes) -> object:
    if not len(blob) > 12:
        raise TypeError('Pixelmator blobs are more than 12 bytes! ')

    magic = blob[:4]
    if not magic == _MAGIC:
        raise TypeError('Pixelmator blobs start with the magic number "4-tP".')

    kind = blob[4:8][::-1]
    if kind in _FORMATS:
        packer, unpacker = _FORMATS[kind]
    else:
        raise TypeError(f'Unknown blob type {kind}.')

    length, = _LENGTH.unpack(blob[8:12])
    data = blob[12:12+length]
    return unpacker(data)


def make_blob(kind: bytes, *data) -> bytes:
    if kind not in _FORMATS:
        raise TypeError(f'Unknown blob type {kind}.')
    packer, unpacker = _FORMATS[kind]
    data = packer(*data)
    length = _LENGTH.pack(len(data))
    return _MAGIC + kind[::-1] + length + data


def _assertver(kind, want, found):
    if want == found:
        return
    else:
        raise ValueError(f"Expected {kind} version {want}, got {found}")


def vercon(data: dict, version=1):
    _assertver('vercon', version, data['version'])
    return data['versionSpecifiContainer']


def verlist(data: list, version=1):
    _assertver('verlist', version, data[0])
    return data[1]


class RGBA:
    '''
    RGBA color in [0, 255]-space.
    '''

    def __init__(self, r=0, g=0, b=0, a=255):
        '''
        Accepts RGBA values, tuple or hex string.
        '''
        if isinstance(r, (tuple, list)):
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

    def __iter__(self):
        tup = self.r, self.g, self.b, self.a
        return iter(tup)

    def __repr__(self):
        val = hexbyte(self.r) + hexbyte(self.g) + hexbyte(self.b)
        if self.a != 255:
            val += hexbyte(self.a)
        return f"RGBA('{val}')"

    @classmethod
    def _from_data(cls, data):
        data = verlist(data)
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

    Contains a list of (RGBA, x),
    alongside a list of midpoints
    and the gradient kind.
    '''

    _default_cols = [
        (RGBA('48a0f8'), 0), (RGBA('48a0f800'), 1)
    ]

    def __init__(self, colors=None, midpoints=None, kind=0):
        self.kind = GradientType(kind)

        self.colors = colors or self._default_cols
        x0 = -1
        for c, x in self.colors:
            assert x0 < x
            x0 = x

        if midpoints is None:
            midpoints = []
            for i in range(len(self.colors) - 1):
                c1, x1 = self.colors[i]
                c2, x2 = self.colors[i+1]
                midpoints.append((x1 + x2)/2)
        self.midpoints = midpoints

    def __repr__(self):
        vals = []
        if self.colors != self._default_cols:
            vals.append(repr(self.colors))

        midpoints_default = True
        for i in range(len(self.colors) - 1):
            c1, x1 = self.colors[i]
            c2, x2 = self.colors[i+1]
            m_apparent = (x1 + x2)/2
            if self.midpoints[i] != m_apparent:
                midpoints_default = False
                break

        if not midpoints_default:
            vals.append(repr(self.midpoints))

        if self.kind != 0:
            vals.append(str(self.kind))

        return f"Gradient({', '.join(vals)})"

    @classmethod
    def _from_data(cls, data):
        data = verlist(data)
        assert data['csr'] == 0
        colors = [verlist(i) for i in data['s']]
        colors = [
            (RGBA(r*255, g*255, b*255, a*255), x)
            for (r, g, b, a), x in colors
        ]
        return cls(colors, data['m'], data['t'])

    def _to_data(self):
        data = {'csr': 0}
        data['m'] = list(self.midpoints)
        data['s'] = [
            [1, [[c.r/255, c.g/255, c.g/255, c.a/255], x]]
            for c, x in self.colors
        ]
        data['t'] = int(self.kind)
        return [1, data]
