'''
RasterLayer object, bound to a PXD file.
'''

from .helpers import num
from .layer import Layer


class RasterLayer(Layer):
    def _repr_info(self):
        yield '{} × {}px'.format(
            num(self.width), num(self.height))
        yield from Layer._repr_info(self)