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
- `flags` (`UI64`) is 64 bits defining various flags for the layer.