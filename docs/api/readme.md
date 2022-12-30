# `pxdlib` API

To read or write to a PXD file, use `PXDFile`. You can read the file at any time, and edit using a `with` block.

```python
from pxdlib import PXDFile
pxd = PXDFile(path_to_file)
layer = pxd.find('Rectangle Layer')
x, y = layer.position
with pxd:
    layer.position = (x+20, y-20)
```

## Accessing a document

The [`PXDFile`](/docs/api/PXDFile.md) itself has a variety of properties that may be accessed; it also exposes methods to obtain layers, which are various subclasses of [`Layer`](/docs/api/Layer.md). Also of note are [`Color` and `Gradient` objects](/docs/api/structures.md)

## Errors

Errors specific to `pxdlib` – and not, say, an invalid function call type – are given as `pxdlib.PixelmatorError` or a subclass thereof; see [`errors.py`](/pxdlib/errors.py) for a full list. 

A `VersionError` is raised when Pixelmator has (very likely) released a new version that `pxdlib` does not support.

A `DatabaseModeError` is raised when a `pxd` file is not open for editing when it should be (or vice versa). The best way to edit a `pxd` file is inside the `with` block, as shown at the top of the document. You can also use `.open()` and `.close()` and read the mode with `.can_write`, if you wish.

## A note on modification

One thing that should be made clear is that the `.pxd` format is database-like. In other words, data objects used directly reference the file; if you want to save a copy, you are best physically duplicating the `.pxd` with `shutil.copytree` or somesuch (_not_ `copy` – as the [documentation](/docs/pxd/) shows, `.pxd` files are actually folders).

Note that the only way to modify a Pixelmator file is to directly set a property on `PXDFile` or `Layer` by `a.b = c` (or `+=`, `-=` etc for numeric properties). If such a property is a list or dictionary, you have to extract that property, modify it, then re-add it.
