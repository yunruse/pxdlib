# `pxdlib` changelog

## Alpha

### 0.1.0 "Noël" (2022-12-25)

- Various bug fixes and improved typing.
- Supports Pixelmator Pro updates:
    - 3.2.0: `VideoLayer` added. (Currently a stub; video-specific details cannot be edited.)
    - 2.3.6: Modern `.pxd` documents may be compressed. (pxdlib now works with them.)

- Added `python -m pxdlib`, a formalised CLI tool for pxdlib, with arguments:
  - Tree display: `-INPF`, `-K key`
  - Layer organisations: `-0`

- `PXDFile` improvements:
    - Added `.open_in_pixelmator()` and `.reload()` helper methods.
    - Changed `pxd.closed` to `pxd.can_write` (and tightened up database checks).

- `Layer` improvements:
    - Vastly improved `repr()` experience
    - Can set the `placeholder` flag for layers considered placeholder assets with a + icon in the layer list.

- `TextLayer` improvements:
    - Renamed `.rawText` to `.raw_text` (still read-only)
    - Added `.text`, a rich-formatted text (currently read-only)

- Technical changes:
    - Various re-architecturings of documentation and library for clarity.
    - Added `pxdlib.plist` internal library for manipulating PLISTs (as used by `TextLayer`).

### 0.0.5

This will probably be the last update for a while until I figure out raster and vector stuff. Until then, however, I've been using this in another project, so I've tried to tighten the API as much as possible. 

- Various bug fixes.
- Added `recurse` keyword (default `True`) to `pxd.find`, `layer.find`.
- Added `pxd.copyto` as a wrapper to `shutil`.
- `layer.copyto` adds ` (Copy)`, ` (Copy 2)`, etc to avoid duplicate names.
- Renamed `RGBA` to `Color`.
- Added `Color.from_{rgb,hsv,hls,yiq}` class methods to align with `colorsys`.
- Improved `Gradient` API, repr.
- Added `.height`, `.width` convenience properties for both `Layer` and `PXDFile`.
- Disallowed setting `layer.size`: will re-enable individually for raster, vector, etc as convenience wrappers for transformation.
- Added `layer.x`, `layer.y` convenience properties.
- Tweaked `layer.position` to be relative to the top left, not bottom left.
- Added a binding class to `layer.styles` such that `.append` (etc) work.
- Auto-set `fillType` based on if a style has a `gradient` provided.
- Added `CENTER`, `TOPLEFT`, `BOTTOM` (etc) for use in `gradientPosition`.
- The beginnings of a `layer.adjusts` property, a library of tweaks and dials that allows, say, `layer.adjusts.white_balance.tint = -0.4`. (Not completed!)

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
