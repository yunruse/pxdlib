'''
A little Swiss Army Knife for PXD files.

Currently needs actual implementation!
'''
import argparse
import pxdlib

parser = argparse.ArgumentParser()

parser.add_argument('--clean', '-c', action='store_true',
                    help='Provides -01d to clean up a .pxd.')

parser.add_argument('--empty', '-0', action='store_true',
                    help='Remove folders with no contents.')
parser.add_argument('--single-item', '-1', action='store_true',
                    help='Replace single-item folders with their'
                    ' contents, automagically ensuring the result'
                    ' keeps any properties applied to the folder.')

# TODO: provide -dd to only check for siblings with the same name
parser.add_argument('--decopy', '-d', action='store_true',
                    help="Remove '(Copy)' from layer names,"
                    ' if no other layer shares the name.')

parser.add_argument('--rename', '-r', nargs=2, metavar=('from', 'to'),
                    help='Find and replace layer names.')


# todo: idk maybe some "set opacity" nonsense?


parser.add_argument('--search', metavar='string', type=str, default=None,
                    help='Only operate on layers with names containing'
                    ' a given search string.')
parser.add_argument('--type', metavar='type', default='all',
                    options='all folders rasters vector text'.split(),
                    help='Only operate on a certain type of layer.')
parser.add_argument('--tag', metavar='color', default='all',
                    options='all red orange yellow'
                            ' green blue purple gray'.split(),
                    help='Only operate on a certain layer tag.')
parser.add_argument('--inside',
                    metavar='layer_name',
                    help='Only operate on a layer or folder.')
