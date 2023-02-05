# `pxdlib` API: Layers

Layer objects contain the bulk of information of a document. They are typically obtained from the [`PXDFile`](/docs/api/PXDFile.md) object itself, though given that layers may have children, they can also be accessed recursively.

At the moment, layers are bound to the `PXDFile` object — they may not be moved about, created or destroyed. Hopefully this functionality will be updated in the near future. 

A layer will never be a direct `Layer` object, but rather one of its four subclasses, [`GroupLayer`](#GroupLayer), `VectorLayer`, `RasterLayer` or `TextLayer`. However, many common attributes are shared between each type.

## Layer
<a id="Layer"></a>

Layers contain the following pointers:

- `pxd`, the `PXDFile` to which they belong. (This cannot be changed.)
- `parent`, which is the `pxd` if the layer is a top-level layer, or the layer to which it belongs. If changed, the layer moves to the top of wherever it is placed.
- `mask`, the layer's mask, if any. If you set a mask, it will delete the current one. If you set a mask to an existing layer, it will move it from its original position.

Layers have the methods:

- `delete()`, which irrevocably deletes the layer and its children. Note that no attributes can be read or written after this is done.
- `copyto(parent, asmask=False) -> Layer`, which copies a layer to the top of a new parent and returns it. (The name has ` (Copy)` or similar appended if needed.)

Layers also have the following shared attributes, all of which can be set:

- `name`, the layer's given visible name.
- `opacity`, an integer in the range [0, 100].
- `is_visible` (`bool`).
- `is_locked` (`bool`). Prevents the layer from being clicked on (useful for editing).
- `is_mask` (`bool`). If true, the layer is the mask for its parent.
- `is_clipping`, (`bool`). Clipping masks appear "on top" of the layer below them, inheriting the opacity of this layer.
- `position` (also `x` and `y`), the x and y coordinates of the center of the layer, in pixels such that the origin is the bottom-left.
- `angle`, a float in degrees in the range [0, 360).
- `blendMode` is an enumerable from `pxdlib.BlendMode`, indicating how the text blends with content behind it.
- `tag` is an enumerable from `pxdlib.LayerTag` (an integer from 0 through 7), indicating the color tag of the layer. By default it is 0 (no tag).
- `styles` is a list of [`Style`](/docs/api/styles.md#styles) objects applied to the layer.
- `adjusts` is a series of [`color adjustments`](/docs/api/styles.md#adjusts) applied to the layer.

## GroupLayer
<a id="GroupLayer"></a>

A `GroupLayer` contains nothing other than its children. It has one attribute:

- `size` (also `width` and `height`), the width and height of the layer in pixels. This is read-only and simply gives the bounding box of its contents.

Like with `PXDFile`, children layers can be found with:

- `children`, a list of the direct children:
- `all_layers()` provides a list of _all_ layers in the group;
- `find(name)` will find the first child layer with a given name.

## VectorLayer
<a id="VectorLayer"></a>

A `VectorLayer` contains a series of shapes. (Currently, these are not accessible.)

Attributes include:

- `size` (also `width` and `height`), the width and height of the layer in pixels.This is currently read-only.

## RasterLayer
<a id="RasterLayer"></a>

A `RasterLayer` contains a raster image, a grid of pixels. (Currently, this is not accessible.)

Attributes include:

## TextLayer
<a id="TextLayer"></a>

A `TextLayer` contains formatted text. It may also contain a single shape, the path along which the text moves.

Attributes include:

- `size` (also `width` and `height`), the width and height of the layer in pixels. This is currently read-only.
- `raw_text`, the text without formatting. This is currently read-only.
- `text`, the text with formatting. This takes the form of a list of 2-tuples, the first element being the text, the second the text style (`TextStyle`).


### TextStyle
A `TextStyle` object has the following properties (most of them fairly self-evident):

- `color` ([`Color`](soiudfhsdifsdf))
- `bold` (`bool`)
- `italic` (`bool`)
- `underline` (`bool`)
- `strikethrough` (`bool`)
