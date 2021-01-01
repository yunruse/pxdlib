# `pxdlib` API: Layers

Layer objects contain the bulk of information of a document. They are typically obtained from the [`PXDFile`](/docs/api/PXDFile.md) object itself, though given that layers may have children, they can also be accessed recursively.

At the moment, layers are bound to the `PXDFile` object — they may not be moved about, created or destroyed. Hopefully this functionality will be updated in the near future. 

A layer will never be a direct `Layer` object, but rather one of its four subclasses, [`GroupLayer`](#GroupLayer), `VectorLayer`, `RasterLayer` or `TextLayer`. However, many common attributes are shared between each type.

<a id="Layer"></a>
## Layer

<a id="GroupLayer"></a>
## GroupLayer

<a id="VectorLayer"></a>
## VectorLayer

<a id="RasterLayer"></a>
## RasterLayer

<a id="TextLayer"></a>
## TextLayer

