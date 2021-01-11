# `pxdlib` API

To read or write to a PXD file, simply do:

```python
from pxdlib import PXDFile
pxd = PXDFile(path_to_file)
```

The [`PXDFile`](/docs/api/PXDFile.md) itself has a variety of properties that may be accessed; it also exposes methods to obtain layers, which are various subclasses of [`Layer`](/docs/api/Layer.md).

One thing that should be made clear is that the `.pxd` format is database-like. In other words, data objects used directly reference the file; if you want to save a copy, you are best physically duplicating the `.pxd` with `shutil.copytree` or somesuch (_not_ `copy` – as the [documentation](/docs/pxd/) shows, `.pxd` files are actually folders).

If you attempt to modify the `pxd` file, you will receive an `io.UnsupportedOperation` error unless the `PXDFile` is open for modification. The best way to access this is using the `with` block:

```python
with pxd:
    pass # Modifications
# Modifications will be immediately applied as soon as block closes
```

Note that the only way to modify a Pixelmator file is to directly set a property on `PXDFile` or `Layer` by `a.b = c` (or `+=`, `-=` etc for numeric properties). If such a property is a list or dictionary, you have to extract that property, modify it, then re-add it. (Otherwise it gets a little hazy.)
