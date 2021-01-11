# Pixelmator Pro (.pxd) format: Layer styles

Inside [`layer_info`](/docs/pxd/#sql), each layer may optionally have the keys [`styles-data`](#styles-data), [`color-adjustments`](#color-adjustments) and [`effects-data`](#effects-data) tables. (If present, the respective tool will be semi-highlighted in Pixelmator Pro).

All of the three are UTF-8 encoded JSON dictionaries. ([Structures](/docs/pxd/readme.md#json) such as 'vercon' and 'verlist' will crop up here.) They are as follows:

<a id="styles-data"></a>
## Styles data

The `styles-data` key is a verlist. The dictionary inside contains six keys:

- `csr`, nominally 0
- `ctx`, a verlist containing what appears to be data on the color profile. It appears to be consistent on my device, so I think it's no big issue if we label it: (unknown)
- `f` (fill), `s` (stroke), `S` (shadow) and `i` (inner shadow).

The four single-letter keys above are each lists of their respective style effects (as you can have more than one). Each style effect is a verlist containing a dictionary.

Style effects have the following properties:

- `id`, a UUID;
- `C` and `V`, which always seem to be 1;
- `E`, which is 0 if disabled and 1 if enabled;
- `o`, the opacity from 0 to 1;
- `B`, the blend mode. (See `BlendMode` under [`enums.py`](/pxdlib/enums.py) for a list of values.) Note that `S` (shadow) effects do not have a `B`.
- `fT`, the fill type (for `f` and `s`.) This is 0 if a color is used and 1 if a gradient is used. Note that _all_ layer effects will contain gradient data, even if they can't actually display gradients.
- `c`, the color (for all style effects), a standard [color](/docs/pxd/readme.md#json).
- `gSP` and `gEP`, the coordinates for the source and end points for gradients. These are two-lists of the x-y coordinates in relative coordinates to the bounding box (so `[0.5, 0.5]` is the center).
- `g`, the gradient (for `f` and `s` effects), which specifies _n_ colors. Like a standard color, this is a verlist containing a dictionary with:
  - `csr`, nominally 0;
  - `t`, the gradient kind (0 being linear, 1 a radial, and 2 angle);
  - `m`, the _n-1_ midpoints. (These are specified where 0 is the very start and 1 the very end, so even if they are all midpoints they will not all be 0.5).
  - `s`, the series of _n_ colors from start to end. Each is a verlist containing the two-list `[[R, G, B, A], x]` (where all are floats from 0 to 1) for the color RGBA and the position x.

For `s` (stroke) effects:

- `sT` is the stroke type (0 regular, 1 dashed, 2 dotted);
- `sP` is the stroke position (0 inside, 1 center, 2 outside);
- `sW` is the stroke width in pixels;

For `S` (shadow) and `i` (inner shadow) effects:

- `b` is the blur (in pixels);
- `d` is the distance (in pixels);
- `a` is the angle used for distance (in radians, from 0 through 2pi);

<a id="color-adjustments"></a>
## Color adjustments

The `color-adjustments` key is a verlist (version 2). A few tags are general header info:

- `csr`, nominally 0
- `ctx`, a verlist, which again we shall treat as: (unknown)
- `in`, nominally 0
- `e`, nominally 0

Each effect listed is a also a key in the dictionary: a verlist (nominally version 1) with the keys `V` (always, seemingly, 1), `E` (1 if enabled, else 0), alongside a variety of key-value pairs corresponding to the knobs and dials in each adjustment effect.

If _`i`_ is given, it refers to the "intensity" knob, from 0 to 1, and defaults to 1. Likewise, if _`A`_ is given, it is 1 if the "ML" auto-adjustment is made, and 0 otherwise. Otherwise, unless specified, a value ranges from -1 to +1, corresponding to -100% to +100%, and default to 0.

The fo

- `w`, "White Balance", with _`A`_, `T` (tint) and `t` (temperature);
- `hS`, "Hue & Saturation", with _`A`_, `h` (hue), `s` (saturation) and `v` (vibrance);
- `l`, "Lightness", with _`A`_, `e` (exposure, -2 to +2), `h` (highlights*), `s` (shadows*), `b` (brightness), `c` (contrast) and `B` (black point). *Highlights and shadows are from -2 to +2, but correspond to -100% to +100%.
- `B`, "Color Balance", with _`A`_ and (unknown);
- `ca`, "Selective Color", with _`A`_ and (unknown);
- `L`, "Levels", with `rgb`, `l` (luminance), `r`, `g` and `b`. These five are all vercons with the self-evident tags `white`, `midOfGrayAndWhite`, `gray`, `midOfGrayAndBlack` and `black`. All are from 0 to 1, and should hopefully be in linear order, and default to `[0, 0.25, 0.5, 0.75, 1]`.
- `C` (verlist version 2), "Curves", likewise with tags `rgb`, `l`, `r`, `g` and `b`. These five are all verlists with the tags:
  - `h`, `s` and `l`, nominally 0; unadjustable in Pixelmator.
  - `P`, a list of points defining the curve, by default `[[0, 0], [1, 1]]`.
- `r`, "Replace Color", with the tags _`i`_, `r` (range, 0 to 1), and the colors `s` (source) and `t` (transformed);
- `b`, "Black & White", with `t` (tone), and `b`, a vercon containing the tags:
  - `saturation`, nominally 0;
  - `red`, `green` and `blue`, -1 to +1;
- `M`, "Color Monochrome", with _`i`_ and `c`, the color;
- `s`, "Sepia", with _`i`_;
- `f`, "Fade", with `c` (nominally 0) and `f` (the intensity, 0 to 1);
- `m`, "Channel Mixer", with `r`, `g` and `b`, all vercons with the tags `red`, `green`, `blue` and `constant`;
- `i`, "Invert", with _`i`_;
- `v`, "Vignette", with `e` (exposure, default 0.5), `b` (black point) and `s` (softness, 0 to 1);
- `S`, "Sharpen", with _`i`_ and `r` (radius, an integer in pixels, from 0 to 100, default 2.5)
- `g`, "Grain", with _`i`_ (default 0.5) and `s` (size, 0 to 2, default 25%).

(Note that you might not see all of these in Pixelmator; some are hidden under 'Customize' by default.)

<a id="effects-data"></a>
## Effects data

The `effects-data` key is a verlist. (unknown)