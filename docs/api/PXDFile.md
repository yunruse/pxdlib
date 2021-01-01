# `pxdlib` API: PXDFile

The `PXDFile` object contains a variety of metadata about the Pixelmator document, alongside the layers contained that make up the image.

## Methods

- `open()`. Starts a transaction to modify the document. Changes will only be made on `close()`.
- `close()`. Closes a transaction and commits any changes made. `open()` and `close()` are useful in certain edge cased, but it is recommended to use a `with pxd` block.

## Metadata

The following metadata may be read from and written to:

- `guides` is a list of the guides used for visual alignment. They are given as a list of two-tuples (is_vertical, r): for example, the guide _y=10_ would be `(True, 10)` and _x=-4_ would be `(False, -4)`.
