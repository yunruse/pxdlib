# `pxdlib` changelog

## Alpha

### 0.0.3

- Added the `layer.styles` property, a list of `Fill`, `Stroke`, `Shadow` and `InnerShadow` objects, supported by the `RGBA` and `Gradient` structures.
- Tightened up data to avoid data redundancy when, say, multiple layers are being referenced.
- Add `layer.pxd` and `layer.parent` properties, the latter of which may be modified.

### 0.0.2

- Various bug fixes.
- `PXDFile.guides` returns and accepts `([x...], [y...])` rather than `[(is_vertical, r)...]`

### 0.0.1

- First public release.
- Basic pxd opening and metadata.
- Basic layer attributes: name, position, opacity, flags.
- Unformatted text may be viewed but not changed.
