# `pxdlib` API

To read or write to a PXD file, simply do:

```python
from pxdlib import PXDFile
pxd = PXDFile(path_to_file)
```

The [`PXDFile`](/docs/api/PXDFile.md) itself has a variety of properties that may be accessed; it also exposes methods to obtain layers, which are various subclasses of [`Layer`](/docs/api/Layer.md).
