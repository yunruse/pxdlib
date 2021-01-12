# pxdlib (Alpha 0.0.3)

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

## Development

As `pxdlib` is available on PyPI, it will be updated in `production` only when a new version is available. The reverse-engineering document, however, will be kept up-to-date in `production` as behaviour is confirmed.

Until the library is considered "done", it will not be confirmed to work on any specific Pixelmator version other than "the latest". I will consider `pxdlib` "done" when:

- raster layers are accessible in a format which is compatible with a good raster-manipulating API;
- vector layers are fully modifiable;
- text layers can be modified, at least with the common formatting capabilities;
- all effects and filters are documented and available;
- layers can be created and destroyed;

and all of the above is formally tested with a specially-created document.

A changelog is available [here](https://github.com/yunruse/pxdlib/blob/production/docs/changelog.md).
