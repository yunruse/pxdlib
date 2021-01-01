# pxdlib (Alpha 0.0.1)

`pxdlib` is a library intended for deciphering and manipulating `.pxd` files, used by the image editor [Pixelmator Pro]. Grab Python 3.6 or above and `pip install pxdlib`!

Documentation exists for the [API], and a much longer set of documentation exists for the [reverse-engineering] of the `.pxd` format.

[Pixelmator Pro]: https://pixelmator.com/pro/
[API]: docs/api/readme.md
[reverse-engineering]: docs/api/readme.md

`pxdlib` can be used for a variety of purposes. For example, if you have designed a graph,
you may automagically manipulate coordinates as:

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