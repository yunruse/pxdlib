'''
Basic structures
'''

from struct import Struct

_MAGIC = b'4-tP'
_LENGTH = Struct('<i')


def _bare(fmt, mul=None):
    fmt = Struct(fmt)

    def packer(*data):
        if mul is not None:
            data = [x / mul for x in data]
        return fmt.pack(*data)

    def unpacker(data):
        result = fmt.unpack(data)
        if mul is not None:
            result = [x * mul for x in result]
        if len(result) == 1:
            result = result[0]
        return result
    return packer, unpacker


def string_unpack(data):
    length, = _LENGTH.unpack(data[:4])
    return data[4:4+length].decode().replace('\x00', '')


def string_pack(data):
    data = data.encode()
    buffer_bytes = -len(data) % 4
    return _LENGTH.pack(len(data)) + data + '\x00' * buffer_bytes


_FORMATS = {
    b'tPTP': _bare('>dd', mul=2),
    b'zSTP': _bare('>dd', mul=2),
    b'zSDB': _bare('<qq'),
    b'lFTP': _bare('<d'),
    b'nrtS': (string_pack, string_unpack),
    b'cpOL': _bare('<H'),
}


def blob(blob):
    if not len(blob) > 12:
        raise TypeError('Pixelmator blobs are more than 12 bytes! ')

    magic = blob[:4]
    if not magic == _MAGIC:
        raise TypeError('Pixelmator blobs start with the magic number "4-tP".')

    kind = blob[4:8]
    if kind in _FORMATS:
        packer, unpacker = _FORMATS[kind]
    else:
        raise TypeError(f'Unknown blob type {kind}.')

    length, = _LENGTH.unpack(blob[8:12])
    data = blob[12:12+length]
    return unpacker(data)


def make_blob(kind, *data):
    if kind not in _FORMATS:
        raise TypeError(f'Unknown blob type {kind}.')
    packer, unpacker = _FORMATS[kind]
    data = packer(*data)
    length = _LENGTH.pack(len(data))
    return _MAGIC + kind + length + data


def _assertver(kind, want, found):
    if want == found:
        return
    else:
        raise ValueError(f"Expected {kind} version {want}, got {found}")


def vercon(data, version=1):
    _assertver('vercon', version, data['version'])
    return data['versionSpecifiContainer']


def verlist(data, version=1):
    _assertver('verlist', version, data[0])
    return data[1]
