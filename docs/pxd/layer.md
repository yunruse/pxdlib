# Pixelmator Pro (.pxd) format: Layers

The layer object is exposed in three [tables](/docs/pxd/#sql). `document_layers` contains two identifiers:
- `id`, an integer, is used to link it to the `layer_tiles` and `layer_info` tables;
- `identifier`, an UUID string, is used to link the document to other layers.

The `document_layers.type` is an integer indicating the layer's type. It is one of:

1. A raster layer. Only these layers will have a corresponding `layer_tiles` table; if a non-empty layer, the layer’s contents are stored in the data folder.
2. A text layer.
3. A vector layer.
4. A group layer, containing other layers.

It's not too hard to construct a tree of layers with `parent_identifier` and `index_at_parent`; `parent_identifier` is null for top-level layers. However, take note that any layer may have a single child in the form of a raster layer as a visibility mask. (See the `flags` attribute below for how to identify this.)

Below are a list of attributes which can be obtained from `layer_info`.

## Common attributes

Every layer will have the following attributes:

- `name` ([`Strn`](/docs/pxd/#blobs)) is the visual name of the layer;
- `opacity` (`LOpc`) is a big-endian (!) short integer from 0 to 100 giving the layer's opacity from 0 through 100;
- `flags` (`UI64`) is a 64-bit integer representing a bitmask. From the least significant bit:
  - The first bit defined if a layer is visible;
  - The second bit defines if a layer is locked;
  - The third bit is unknown;
  - The fourth bit defines if a layer is a clipping mask (i.e. will mask onto the layer below);
  - The fifth bit defines if a layer is a mask (i.e. defines the mask of its parent layer);
  - The sixth bit is unknown;
  - The seventh bit is on iff the layer is a raster;
- `color-value` is a raw integer (i.e. _not_ a blob) defining the colour (aka tag) given to the layer: 0 if untagged, or 1-7 for various tags.
- `blendMode` (`Blnd`) are four characters (in reverse order) which define the blend mode. (See [`layer.py`](/pxdlib/layer.py) for a list of values known.)
- `position` ([`PTPt`](/docs/pxd/#blobs)) points to the centre of the layer.
- `size` ([`PTSz`](/docs/pxd/#blobs)) is the size of the layer in pixels.
- `scale` ([`PTPt`](/docs/pxd/#blobs)), (unknown).
- `backingScale` ([`PTFl`](/docs/pxd/#blobs)), (unknown).
- `anchorPoint` ([`PTPt`](/docs/pxd/#blobs)), (unknown).
- `angle` ([`PTFl`](/docs/pxd/#blobs)), in degrees from -360 to 0. Nominally 0 except for text layers.
- `transform` (`Trns`), (unknown).
- `user-info-data`, a UTF-8 encoded PLIST file, nominally empty.

Optionally present are the `styles-data`, `color-adjustments` and `effects-data` attributes (unknown).

## Raster layers

(unknown)

## Text layers

(unknown)

## Vector layers

(unknown)