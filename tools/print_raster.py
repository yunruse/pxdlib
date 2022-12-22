from pxdlib import *
from pxdlib.structure import _blob, _FORMATS
from pxdlib.plist import *
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('file', help='.pxd file')
parser.add_argument('layer', help='Name(s) of layer')
args = parser.parse_args()

pxd = PXDFile(args.file)
layer = pxd.find(args.layer)
assert isinstance(layer, RasterLayer)

raster = print(layer._raster_info())