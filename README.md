# pxdlib (Alpha 0.0.4)

`pxdlib` is a library intended for deciphering and manipulating `.pxd` files, used by the image editor [Pixelmator Pro]. Grab Python 3.6 or above and `pip install pxdlib`!

Documentation exists for the [API], and a much longer set of documentation exists for the [reverse-engineering] of the `.pxd` format.

[Pixelmator Pro]: https://pixelmator.com/pro/
[API]: https://github.com/yunruse/pxdlib/blob/production/docs/api/readme.md
[reverse-engineering]: https://github.com/yunruse/pxdlib/blob/production/docs/pxd/readme.md

`pxdlib` can be used for a variety of purposes. For example, if you have designed a graph, you may automagically manipulate coordinates as:

```python
from pxdlib import PXDFile

P0, T0 = 50, 100

COORDS = dict()
with open('data.csv') as f:
    for line in f.readlines():
        name, P, T = line.strip().split(',')
        COORDS[name] = P0 + float(P), T0 + float(T)

with PXDFile('graph.pxd') as pxd:
    for l in pxd.all_layers():
        if l.name in COORDS:
            l.position = COORDS[l.name]
```

## Features

**At the moment, pxdlib can:**
- Navigate layer structure
- Modify common properties - size, position, opacity, style, gradients

**In the future, it is intended to be able to:**
- Read and write raster layers in a convenient interoperable format
- Modify vector layers
- Modify common text properties
- Destroy and create layers
- Have formal testing and be kept up-to-date

**There is currenty no scope for Pixelmator features such as:**
- exporting or converting – this is complicated!
- using any ML/AI features in Pixelmator 

## Development

The `production` branch relates to features available in PyPI; `development` is up-to-date.

Any and all issues are completely welcomed -- especially if `pxdlib` breaks on newer versions of Pixelmator!

A changelog is available [here](https://github.com/yunruse/pxdlib/blob/production/docs/changelog.md).
