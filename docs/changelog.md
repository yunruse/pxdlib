# `pxdlib` changelog

## Alpha

### 0.0.5

Note: This will be the last update for a little while. The vector and raster formats are tough nuts to crack, so I'm going to come to it with fresh eyes.

- Various bug fixes.
- Added `pxd.copyto` as a wrapper to `shutil`.
- Renamed `RGBA` to `Color`.
- Added `Color.rgb`, `.hsv`, `.hls`, `.yiq` class methods to align with `colorsys`.
- Improved `Gradient` API, repr.
- Added `.height`, `.width` convenience properties for both `Layer` and `PXDFile`.
- Added the `layer.adjusts` property, a library of tweaks and dials that allows, say, `layer.adjusts.white_balance.tint = -0.4`.

### 0.0.4 (2020-01-15)

- Various bug fixes.
- Added `PixelmatorError`, and tightened up error raising, in particular with `layer.mask`.
- Improved `repr(layer)`.
- Allowed very limited creation of new layers eg `GroupLayer(parent)`. (It's a bit buggy though.)
- Added settable property `pxd.size`.
- Added `layer.delete` and `layer.copyto(parent)`, and thereby added the ability to set `layer.parent` to be in a different `PXDFile`.

### 0.0.3 (2021-01-12)

- Added the `layer.styles` property, a list of `Fill`, `Stroke`, `Shadow` and `InnerShadow` objects, supported by the `RGBA` and `Gradient` structures.
- Tightened up data to avoid data redundancy when, say, multiple layers are being referenced.
- Add `layer.pxd`, `layer.mask` and `layer.parent` properties, the last of which may be modified.
- Fixed `layer.children` such that any masks are not shown.

### 0.0.2 (2021-01-08)

- Various bug fixes.
- `PXDFile.guides` returns and accepts `([x...], [y...])` rather than `[(is_vertical, r)...]`

### 0.0.1 (2021-01-01)

- First public release.
- Basic pxd opening and metadata.
- Basic layer attributes: name, position, opacity, flags.
- Unformatted text may be viewed but not changed.
