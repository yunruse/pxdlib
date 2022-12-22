'''
A little Swiss Army Knife for PXD files.

Currently needs actual implementation!
'''
import argparse
from sys import stderr
from typing import Callable, Generator
from pxdlib import PXDFile, GroupLayer, Layer
from pxdlib.structure import blob

_exit = exit
def exit(code: int, reason: str):
    print(reason, file=stderr)
    _exit(code)

parser = argparse.ArgumentParser()
parser.add_argument('file', help='The .pxd file to operate on')



search = parser.add_argument_group('Provide a filter that all actions will only apply to')
# search.add_argument('--search',metavar='string', type=str, default=None,
#                     help='Only operate on layers with names containing'
#                     ' a given search string.')
# search.add_argument('--type', metavar='type', default='all',
#                     choices='all folders rasters vector text'.split(),
#                     help='Only operate on a certain type of layer.')
# search.add_argument('--tag', metavar='color', default='all',
#                     choices='all red orange yellow'
#                             ' green blue purple gray'.split(),
#                     help='Only operate on a certain layer tag.')
search.add_argument('--inside',
                    metavar='layer_name',
                    help='Only operate on a layer or group by this name.')



info = parser.add_argument_group('Display info in a tree')
info.add_argument(
    '--no-indent', dest='indent', action='store_false',
    help='Do not indent to indicate layer structure')
info.add_argument(
    '--layer-info', '-I', action='store_true',
    help='Show most relevant layer information')
info.add_argument(
    '--layer-name', '-N', action='store_true',
    help='Show layer names')
info.add_argument(
    '--layer-position', '-P', action='store_true',
    help='Show layer position and size')
info.add_argument(
    '--layer-flags', '-F', action='store_true',
    help='Show layer flags')
info.add_argument(
    '--layer-keys', '-K',
    nargs='*', metavar='KEYS', default=None,
    help='Show layer metadata with KEYS (provide `all` for all)')

def process_display(args):
    args.do_display = any((
        args.layer_name,
        args.layer_info,
        args.layer_position,
        args.layer_flags,
        args.layer_keys,
    ))
    def display(layer: Layer | PXDFile):
        if isinstance(layer, Layer):
            if args.layer_name:
                yield layer.name
            if args.layer_position:
                yield '({}, {}), {}×{}'.format(
                    layer.x, layer.y, layer.width, layer.height)
            if args.layer_flags:
                yield repr(layer._flags)
            if args.layer_keys:
                def display_blob(k):
                    v = layer._info(k)
                    if isinstance(v, bytes) and v.startswith(b'4-tP'):
                        try:
                            v = blob(v)
                        except TypeError:
                            pass
                    return v
                keys = args.layer_keys
                if keys == ['all']:
                    keys = list(layer._info_keys())
                indent = max(map(len, keys))
                yield '\n'.join(
                    f'{k.rjust(indent)}: {display_blob(k)!r}' for k in keys
                )
        if args.layer_info:
            yield repr(layer)
    args.display_func = display

def display_tree(
    layer: PXDFile | Layer,
    func: Callable[[PXDFile | Layer], Generator[str, None, None]],
    do_indent = True,
    level: int = 0,
):
    info = ' '.join(func(layer))
    if info:
        if do_indent:
            print('    ' * level, info)
        else:
            print(info)
    if isinstance(layer, (PXDFile, GroupLayer)):
        for l in layer.children:
            display_tree(l, func, do_indent, level+1)



# organise = parser.add_argument_group('Re-organise layers')
# organise.add_argument('--clean', '-c', action='store_true',
#                     help='Provides -01ds to clean up a .pxd.')

# organise.add_argument('--empty', '-0', action='store_true',
#                     help='Remove groups with no contents.')
# organise.add_argument('--single-item', '-1', action='store_true',
#                     help='Replace single-item groups with their'
#                     ' contents, automagically ensuring the result'
#                     ' keeps any properties applied to the folder.')
# organise.add_argument('--decopy', '-d', action='store_true',
#                     help="Remove '(Copy)' from layer names"
#                     ' if they are unique.')
# organise.add_argument('--strip', '-s', action='store_true',
#                     help="Remove extraneous whitespace from layer names.")

# organise.add_argument('--rename', '-r', nargs=2, metavar=('a', 'b'),
#                     help="Replace a with b in all layer names.")

# organise.add_argument('--rename-to-contents',
#                     help="Rename text layers to their contents (if possible).")



if __name__ == '__main__':
    args = parser.parse_args()
    # if args.clean:
    #     args.empty = args.single_item = args.decopy = args.strip = True

    pxd = PXDFile(args.file)

    # TODO: Filter
    if args.inside:
        layer = pxd.find(args.inside)
        if layer is None:
            exit(404, f'No layer named {args.inside!r}')
    else:
        layer = pxd
    

    process_display(args)
    if args.do_display:
        display_tree(pxd, args.display_func, args.indent)
