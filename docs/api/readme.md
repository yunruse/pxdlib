# `pxdlib` API

To read or write to a PXD file, use `PXDFile`. For example:

```python
from pxdlib import PXDFile
pxd = PXDFile(path_to_file)
layer = pxd.find('Rectangle Layer')
x, y = layer.position
with pxd:
    layer.position = (x+20, y-20)
```

## Accessing a document

The [`PXDFile`](/docs/api/PXDFile.md) itself has a variety of properties that may be accessed; it also exposes methods to obtain layers, which are various subclasses of [`Layer`](/docs/api/Layer.md).

## Errors

Errors specific to `pxdlib` – and not, say, an invalid function call type – are given as `pxdlib.PixelmatorError` or a subclass thereof; see [`errors.py`](/pxdlib/errors.py) for a full list. 

Notable is `VersionError`, which indicates that Pixelmator has (very likely) released a new version, and that you should update `pxdlib`.

## A note on modification

One thing that should be made clear is that the `.pxd` format is database-like. In other words, data objects used directly reference the file; if you want to save a copy, you are best physically duplicating the `.pxd` with `shutil.copytree` or somesuch (_not_ `copy` – as the [documentation](/docs/pxd/) shows, `.pxd` files are actually folders).

If you attempt to modify the `pxd` file, you will receive an `io.UnsupportedOperation` error unless the `PXDFile` is open for modification. The best way to access this is using the `with` block, as shown at the top of the document. As soon as the `with` block is closed, the changes are immediately present in the document, ready to be seen in Pixelmator.

Note that the only way to modify a Pixelmator file is to directly set a property on `PXDFile` or `Layer` by `a.b = c` (or `+=`, `-=` etc for numeric properties). If such a property is a list or dictionary, you have to extract that property, modify it, then re-add it.
