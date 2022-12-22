'''
RasterLayer object, bound to a PXD file.
'''

from .helpers import num
from .layer import Layer


class RasterLayer(Layer):
    @property
    def _raster_path(self):
        return self.pxd._edit_dir / 'data' / self._uuid

    def _raster_info(self):
        with open(self._raster_path, 'rb') as f:
            return f.read()

    def _repr_info(self):
        yield '{} × {}px'.format(
            num(self.width), num(self.height))
        yield from Layer._repr_info(self)