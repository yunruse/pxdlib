'''
Basic structures
'''

from struct import Struct

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
