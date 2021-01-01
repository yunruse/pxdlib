import base64
import binascii
import datetime
import json
import os
from pathlib import Path
import sqlite3
import plistlib
import struct

import pxdlib as pxdlib
from pxdlib import blob, vercon, verlist

def hexes(data):
    return binascii.hexlify(data).decode()

def hexdump(data):
    data = hexes(data)
    line = ''
    while data:
        buf, data = data[:8], data[8:]
        print(buf, end=' ')
    print()


if __name__ == '__main__':
    pxd = pxdlib.PXDFile('test/view.pxd')

    def display(layers, s=0):
        for l in layers:
            x, y = l.position
            x, y = int(x), int(y)

            print(f"{' ' * s}{l._id}( {x:4d}, {y:4d}) {l.name:<20} ", end='')
            if isinstance(l, pxdlib.RasterLayer):
                print('raster', l._uuid)

            elif isinstance(l, pxdlib.TextLayer):                    
                print('text: ', end='')
                string = l.getText()
                if len(string) > 30:
                    string = repr(string[:16]) + f'... [{len(string)} chars]'
                else:
                    string = repr(string)
                print(string)

            elif isinstance(l, pxdlib.VectorLayer):
                print('vector')
                data = vercon(json.loads(l._info['shape-shapeData'].decode()))
                data = vercon(data['pathCodableWrappers'][0])
                data = vercon(data['shapePathUnkeyedContainer'][0])
                data = vercon(data['backingStorage'])
                path = base64.b64decode(
                    vercon(data['bezierPath'])['dataFromCGPath']
                )
                print()
                print(path)
                print()
                print(len(path))
                hexdump(path)

            display(l.children(), s+1)

            # Layer debugging here

    display(pxd.layers())

    # PXD debugging here
    pxd.closed = False

