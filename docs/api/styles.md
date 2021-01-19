# `pxdlib` API: Layer styles

<a id="styles"></a>
## Styles

`layer.styles` is a list of `Style` objects. While this cannot be directly instantiated, its subclasses, `Fill`, `Stroke`, `Shadow` and `InnerShadow`, can.

If you want to add, modify or remove a style, set `layer.styles` to a modified list of styles. The order provided is the order styles are displayed; note that Pixelmator has its own quirks with style application. You can remove or add new styles, or modify existing ones.

All `Style` objects contain the following properties:

- `enabled`, a boolean as to if the style is enabled;
- `opacity`, between 0 and 1;
- `blendMode`, a `BlendMode` enum (default `normal`);
- `color`, an `RGBA` object, the color of the fill effect. 

`Fill` and `Stroke` styles contain:

- `fillType`, a `FillType` (`.color`, `.gradient`) defining which is used for display.
- `gradientPosition`, a tuple of two coordinates. These are in relative coordinates, where `[0, 0]` is the top-left and `[1, 1]` the bottom-right.
- `gradient`, a `Gradient` object. This has the properties:
  - `colors`, a list of two-tuples `(RGBA, x)`, where `x` ranges from 0 through 1;
  - `kind`, a `GradientType` (`.linear`, `.radial`, `.angle`);
  - `midpoints`, a list of _n-1_ midpoints from 0 through 1. This tweaks the movement of the color gradient; it defaults to being in the middle of its respective points.

`Stroke` styles also contain:

- `strokeType`, a `StrokeType` (`.regular`, `.dashed`, `.dotted`);
- `strokePosition`, a `StrokePosition` (`.inside`, `.center`, `.outside`);
- `strokeWidth`, the width in pixels.

Both `Shadow` and `InnerShadow` styles contain:

- `blur`, the blur in pixels.
- `distance`, the distance of the shadow from the object in pixels.
- `angle`, in degrees clockwise from north.

<a id="adjusts"></a>
## Color adjustments

Color adjustments are provided by `layer.adjusts`. As `repr(layer.adjusts)` may imply:

    <ColorAdjustments: as listed below>
      .white_balance.temperature = 0.443
      .white_balance.tint = -0.8

one can modify the parameters of each adjustment directly.

Changing a property automatically enables its adjustment, but you can set `layer.adjusts.x.enabled = False` if you want.

Properties are:

- `.white_balance.temperature`: -1 (blue) to +1 (orange), default 0 
- `.white_balance.tint`: -1 (green) to +1 (purple) 
