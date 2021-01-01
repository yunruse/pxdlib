# `pxdlib` API: Layers

Layer objects contain the bulk of information of a document. They are typically obtained from the [`PXDFile`](/docs/api/PXDFile.md) object itself, though given that layers may have children, they can also be accessed recursively.

At the moment, layers are bound to the `PXDFile` object — they may not be moved about, created or destroyed. Hopefully this functionality will be updated in the near future. 

A layer will never be a direct `Layer` object, but rather one of its four subclasses, [`GroupLayer`](#GroupLayer), `VectorLayer`, `RasterLayer` or `TextLayer`. However, many common attributes are shared between each type.

<a id="Layer"></a>
## Layer

<a id="GroupLayer"></a>
## GroupLayer

A `GroupLayer` contains nothing other than its children; its coordinates and size are only given as reference. Identical to `PXDFile`, the following methods and attributes are given:

- `children` is a list of the top-level layers, ordered as seen in the document.
- `all_layers()` provides a list of _all_ layers in the document, ordered as seen in the document.

<a id="VectorLayer"></a>
## VectorLayer

<a id="RasterLayer"></a>
## RasterLayer

<a id="TextLayer"></a>
## TextLayer

