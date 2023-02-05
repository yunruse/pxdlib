# pxdlib (Alpha 0.1.0)

`pxdlib` is a library intended for deciphering and manipulating `.pxd` files, used by the image editor [Pixelmator Pro]. Grab Python 3 and `pip install pxdlib`!

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
- Read/write common properties - size, position, opacity, style, gradients
- Read unformatted text from text layers

**In the future, it is intended to be able to:**
- Read/write vector layers
- Read/write raster layers in a convenient interoperable format
- Read/write text layers' formatting and text
- Destroy and create layers
- Have formal testing and be kept up-to-date

**There is currenty no scope for Pixelmator features such as:**
- exporting or converting – this is complicated!
- using any ML/AI features in Pixelmator 

## Development

Branch `production` is that which is released on PyPi, and `development` is, well, in development.

I tend to update this as I use it for my own projects.

No stability is guaranteed, but please raise issues as soon as you see them and I'll try my best to fix them.

Any and all issues are completely welcomed -- especially if `pxdlib` breaks on newer versions of Pixelmator!

A changelog is available [here](https://github.com/yunruse/pxdlib/blob/production/docs/changelog.md).
