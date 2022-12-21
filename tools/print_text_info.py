from pxdlib import PXDFile, TextLayer, Color
from pxdlib.plist import *
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('file', help='.pxd file')
parser.add_argument('layer', help='Name of layer')
args = parser.parse_args()

self = PXDFile(args.file)
layer = self.find(args.layer)
assert isinstance(layer, TextLayer)

l = layer
s = l.text_styles[0]
c = s._get('color')
for k, v in s._info.items():
    print(k, repr(v))
    if isinstance(v, NSObject):
        for k, v in v.items():
            if k == '$class':
                continue
            print(' -', k, repr(v))