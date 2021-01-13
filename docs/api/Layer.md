# `pxdlib` API: Layers

Layer objects contain the bulk of information of a document. They are typically obtained from the [`PXDFile`](/docs/api/PXDFile.md) object itself, though given that layers may have children, they can also be accessed recursively.

At the moment, layers are bound to the `PXDFile` object — they may not be moved about, created or destroyed. Hopefully this functionality will be updated in the near future. 

A layer will never be a direct `Layer` object, but rather one of its four subclasses, [`GroupLayer`](#GroupLayer), `VectorLayer`, `RasterLayer` or `TextLayer`. However, many common attributes are shared between each type.

<a id="Layer"></a>
## Layer

Layers contain the following pointers:

- `pxd`, the `PXDFile` to which they belong. (This cannot be changed.)
- `parent`, which is the `pxd` if the layer is a top-level layer, or the layer to which it belongs. If changed, the layer moves to the top of wherever it is placed.
- `mask`, the layer's mask, if any. If you set a mask, it will delete the current one. If you set a mask to an existing layer, it will move it from its original position.

Layers have the methods:

- `delete()`, which deletes the layer and its children. Note that no attributes can be read or written after this is done.

Layers also have the following shared attributes, all of which can be set:

- `name`, the layer's given visible name.
- `opacity`, an integer in the range [0, 100].
- `is_visible`, a boolean which specifies if the layer is visible.
- `is_locked`, a boolean. This is only a convenience for the UI – it does not affect whether `pxdlib` can modify the layer!
- `is_mask`, a boolean. If true, the layer is the mask for its parent.
- `is_clipping`, a boolean. If true, the layer is a clipping mask; it clips onto the layer below it.
- `position`, a tuple of the x,y coordinates of the center of the layer, defined in pixels such that the origin is the bottom-left.
- `size`,  a tuple of the w,h size of the layer defined in pixels.
- `angle`, a float in degrees in the range [0, 360). Nominally 0 except for text layers.
- `blendMode` is an enumerable from `pxdlib.BlendMode`.
- `tag` is an enumerable from `pxdlib.LayerTag` (or, an integer from 0 through 7) representing a color tag for user convenience. It is truthy if a tag is applied to the layer.
- `styles` is a list of [`Style`](/docs/api/styles.md#styles) objects.

<a id="GroupLayer"></a>
## GroupLayer

A `GroupLayer` contains nothing other than its children; its coordinates and size are only given as reference. Identical to `PXDFile`, the following methods are given:

- `children` is a list of the child layerss
- `all_layers()` provides a list of _all_ layers in the group;
- `find(name)` will find the first layer with a given name.

<a id="VectorLayer"></a>
## VectorLayer

<a id="RasterLayer"></a>
## RasterLayer

<a id="TextLayer"></a>
## TextLayer

