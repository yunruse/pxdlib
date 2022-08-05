# pxdlib (Alpha 0.0.4)

A (reverse-engineered) library intended for deciphering and manipulating the `.pxd` files used by the image editor [Pixelmator Pro].

Grab Python 3.6 or above and `pip install pxdlib`!

Documentation exists for the [API], and a much longer set of documentation exists for the [reverse-engineering] of the `.pxd` format.

[Pixelmator Pro]: https://pixelmator.com/pro/
[API]: https://github.com/yunruse/pxdlib/blob/production/docs/api/readme.md
[reverse-engineering]: https://github.com/yunruse/pxdlib/blob/production/docs/pxd/readme.md

`pxdlib` can be used for a variety of purposes. For example, its first use case was to automagically manipulate coordinates, a little like:

```python
from csv import reader
from pxdlib import PXDFile

x0, y0 = 50, 100

COORDS = dict()
with open('data.csv') as f:
    for name, x, y in reader(f):
        COORDS[name] = x0 + float(x), y0 + float(y)

with PXDFile('graph.pxd') as pxd:
    for l in pxd.all_layers():
        if l.name in COORDS:
            l.position = COORDS[l.name]

# The file is now saved and modified!
```

## Development

As `pxdlib` is available on PyPI, it will be updated in `production` only when a new version is available.

The reverse-engineering document, however, will be kept up-to-date in `production` as behaviour is confirmed.

## What can't pxdlib do?

The following are future goals:

- a much better file API, which doesn't just operate in-place,
- raster layers are accessible in a format which is compatible with a good raster-manipulating API;
- vector layers are fully modifiable;
- text layers can be modified, at least with the common formatting capabilities;
- all effects and filters are documented and available;
- layers can be created and destroyed;
- the above is all formally tested;
- actually being kept 100% up-to-date;
- backwards compatibility

Thankfully Pixelmator is pretty backwards-compatible, so the basic automation tools – toggling visibility, moving items around – should probably work forever. Maybe.

A changelog is available [here](https://github.com/yunruse/pxdlib/blob/production/docs/changelog.md).
