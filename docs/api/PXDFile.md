# `pxdlib` API: PXDFile

The `PXDFile` object contains a variety of metadata about the Pixelmator document, alongside the layers contained that make up the image.

## Methods

For editing purposes:

- `open()` starts a transaction to modify the document. Changes will only be made on `close()`.
- `close()` closes a transaction and commits any changes made. `open()` and `close()` are useful in certain edge cases, but it is recommended to use a `with pxd` block, which handles both a litle easier.
- `copyto(path, overwrite=False) -> PXDfile` copies the PXD file to a new directory and returns it.

For accessing layers:

- `children -> list` is a list of the top-level layers;
- `all_layers() -> list` provides a list of _all_ layers in the document;
- `find(name) -> Layer` will find the first layer with a given name.

In general, layers are ordered as seen visually in the document.

## Metadata

The following metadata may be read from and written to:

- `size` (also `width` and `height`) is the width and height of the document, in pixels. Layers have the top-left of the document as the origin, and will "stick" to it if resized.
- `guides` is a list of the guides used for visual alignment. They are given as a list of two-tuples (is_vertical, r): for example, the guide _y=10_ would be `(True, 10)` and _x=-4_ would be `(False, -4)`.
- `rulerOrigin` is the x,y coordinate of the origin of the (visual) ruler.
