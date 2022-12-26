# Pixelmator Pro (.pxd) format: Layers

The layer object is exposed in three [tables](/docs/pxd/#metadata).



## `document_layers` info

The `document_layers` table contains essential shared layer info:
- `id` (`INTEGER`): An integer, 
- `identifier` (`TEXT`): the UUID, which is used to uniquely identify the layer, and any other content files it may hold.
- `parent_identifier` (`TEXT`): `null` if a top-level layer; otherwise the parent layer, typically a group. Mask layers (see `flags` below) use this to indicate what they are masking.
- `index_at_parent` (`INTEGER`): The ordering index in a group (lower indices appear at the front).
- `type` (`INTEGER`): One of the following:
  - `1`: A [raster layer](#raster).
  - `2`: A [text layer](#text).
  - `3`: A [vector layer](#vector).
  - `4`: A group layer, containing other layers.
  - `7`: A [video layer](#video).



## Layer attributes `layer_info`

The `layer_info` table contains three properties, providing attributes to layers:
- `layer_id` (`INTEGER`), referencing `document_layers`,
- `key` (`TEXT`),
- `value` (`BLOB`).



### Common attributes
<a id='common' />

Every layer has the following `layer_info` attributes:

- `name` ([`Strn`](/docs/pxd/#blobs)) is the visual name of the layer;
- `opacity` (`LOpc`) is a big-endian (!) short integer from 0 to 100 giving the layer's opacity from 0 through 100;
- `opct-nrm` ([`LDOp`](/docs/pxd/#blobs)) is identical to `opacity`, albeit a float from 0 to 1;
- `flags` (`UI64`) is a 64-bit integer representing a bitmask. It has the following bits:
  - `1 << 0`: Iff a layer is visible
  - `1 << 1`: Iff the layer is locked
  - `1 << 2`: ???
  - `1 << 3`: Iff the layer is a clipping mask (will mask onto the layer below)
  - `1 << 4`: Iff the layer is a mask (defines the mask of its parent)
  - `1 << 5`: ???
  - `1 << 6`: Iff the layer is a raster
  - `1 << 7`: ???
  - `1 << 8`: ???
  - `1 << 9`: Iff the layer is a placeholder (raster or video only); will show a + button to insert user media

- `color-value` is a raw integer (i.e. _not_ a blob) defining the color (aka tag) given to the layer: 0 if untagged, or 1-7 for various tags.
- `blendMode` (`Blnd`) are four characters (in reverse order) which define the blend mode. (See `BlendMode` under [`enums.py`](/pxdlib/enums.py) for a list of values.)
- `position` ([`PTPt`](/docs/pxd/#blobs)) points to the center of the layer.
- `size` ([`PTSz`](/docs/pxd/#blobs)) is the size of the layer in pixels.
- `scale` ([`PTPt`](/docs/pxd/#blobs)), ???
- `backingScale` ([`PTFl`](/docs/pxd/#blobs)), ???
- `anchorPoint` ([`PTPt`](/docs/pxd/#blobs)), ???
- `angle` ([`PTFl`](/docs/pxd/#blobs)), in degrees. Pixelmator displays the angle as _360 - θ_.
- `transform` (`Trns`), the transformation of the layer, independent of its rotation. ???

- `user-info-data`, a UTF-8 encoded PLIST file, nominally empty.
- `content-rep-data`, UTF-8 encoded JSON verlist, nominally `{"s": 1, "b": false, "r": false}` ???

Optionally present are the following attributes:
- [`styles-data`](/docs/pxd/styles.md#styles-data)
- [`color-adjustments`](/docs/pxd/styles.md#color-adjustments)
- [`effects-data`](/docs/pxd/styles.md#effects-data) attributes



### Raster layer attributes
<a id="raster" />

Raster layers do not have any specific `document_info` attributes. Instead, they are referenced by the `layer_tiles` table. Inside the `.pxd` directory structure, the raster data for a layer is stored at `/data/{UUID}` for the given UUID of the layer. See [text.md](/docs/pxd/rasterData.md) for a description of this format.



## Text layers
<a id="text" />

Text layers also have the following `document_info` attributes:

- `text-version` ([`SI16`](/docs/pxd/#blobs)) is nominally one;
- `text-layerType` ([`SI16`](/docs/pxd/#blobs)) is either 0 (regular text) or 2 (path text). I haven't observed type 1 in the wild.
- `text-nameIsDynamic` ([`SI16`](/docs/pxd/#blobs)) is a boolean that tells Pixelmator whether to dynamically rename the layer according to the text contents. It defaults to one, and changes to zero whenever the label is changed manually (in Pixelmator or in `pxdlib` :)
- `text-verticalAlignment` ([`SI16`](/docs/pxd/#blobs)) is either 0 (top), 1 (middle) or 2 (bottom).
- `text-widthAutosizable` ([`SI16`](/docs/pxd/#blobs)) is another boolean, and it similarly defaults to one and changes to zero when the user has manually sized the textbox (so that text should wrap rather than keep going).
- `text-insets` ([`PTSz`](/docs/pxd/#blobs)) is the horizontal and vertical padding for wrapping. It is nominally `[4.0, 4.0]` for regular text and `[0.0, 0.0]` for path text.
- `text-stringData`, a UTF-8 encoded [vercon](/docs/pxd/#json) with one entry: `StringNSCodingData`, a base-64 encoded binary PLIST, in which most of the text data is stored. See [layer_text.md](/docs/pxd/layer_text.md) for more info.

For path text (`text-layerType` of 2), the following attributes are also found:

- All three of `text-layer{Start,Middle,End}PointOnPath` ([`PTPt`](/docs/pxd/#blobs)) are the locations of the anchors of the text, coordinates in pixels from the bottom left of the bounding box of the path.
- `text-pathData` is a [vercon](/docs/pxd/#json) with one entry: `dataFromCGPath`, a base-64 encoded path object. (unknown)



## Vector layers
<a id='vector' />

Text layers also have the following `document_info` attributes:

- `shape-shapeData`, a [vercon](/docs/pxd/#json) containing the following tags:
  - `identifier` and `content-identifier`, both UUIDs;
  - `geometry` ???,
  - `pathCodableWrappers`, a [vercon](/docs/pxd/#json) ???



## Video layers
<a id='video' />

Video layers have the following `document_info` attributes:
- `video-params-data`: a UTF-8 encoded [vercon](/docs/pxd/#json) ???

The media is stored at ???