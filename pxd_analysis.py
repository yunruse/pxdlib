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
from pxdlib import blob, verb, RGBA

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

    def displays(layers, s=0):
        for l in layers:
            display(l, s)

    def display(l, s):
        x, y = l.position
        x, y = int(x), int(y)

        name = '<Mask>' if l.is_mask else l.name

        print(' '*s + f'{repr(l)} ( {x:4d}, {y:4d}) ', end='')
        if isinstance(l, pxdlib.RasterLayer):
            uuid = l._uuid.split('-')[0]
            print(uuid)

        elif isinstance(l, pxdlib.TextLayer):
            string = l.getText()
            if len(string) > 30:
                string = repr(string[:16]) + f'... [{len(string)} chars]'
            else:
                string = repr(string)
            print(string)

        elif isinstance(l, pxdlib.VectorLayer):
            print()
            data = verb(json.loads(l._info('shape-shapeData')))
            data = {}
            for k, v in data.items():
                print('-', k, v)
        else:
            print()
        if l.mask:
            display(l.mask, s+2)

        # Layer debugging here
        for style in l.styles:
            data = style._dict
            data = {}
            for k, v in data.items():
                k2 = pxdlib.styles._STYLE_TAGS.get(k)
                if k2:
                    v2 = getattr(style, k2, None)
                    if v2 is None:
                        k2 = None
                    else:
                        v = v2
                print(f'{k:<5} {k2 or "":<17} {repr(v)}')
            print(style)

        # End layer debugging
        
        if isinstance(l, pxdlib.GroupLayer):
            displays(l.children, s+1)

    l = pxd.children[0]
    displays(pxd.children)
    layers = pxd.all_layers()

    # PXD debugging here

