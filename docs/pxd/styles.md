# Pixelmator Pro (.pxd) format: Layer styles

Inside [`layer_info`](/docs/pxd/#sql), each layer may optionally have the keys [`styles-data`](#styles-data), [`color-adjustments`](#color-adjustments) and [`effects-data`](#effects-data) tables. (If present, the respective tool will be semi-highlighted in Pixelmator Pro).

All of the three are UTF-8 encoded JSON dictionaries. ([Structures](/docs/pxd/readme.md#json) such as 'vercon' and 'verlist' will crop up here.) They are as follows:

<a id="styles-data"></a>
## Styles data

The `styles-data` key is a verlist. The dictionary inside contains six keys:

- `csr`, nominally 0
- `ctx`, a verlist containing what appears to be data on the color profile. It appears to be consistent on my device, so I think it's benign if we leave it (unknown)
- `f` (fill), `s` (stroke), `S` (shadow) and `i` (inner shadow).

The four single-letter keys above are each lists of their respective style effects (as you can have more than one). Each style effect is a verlist containing a dictionary.

Style effects have the following properties:

- `id`, a UUID;
- `E`, which is 0 if disabled and 1 if enabled;
- `o`, the opacity from 0 to 1;
- `B`, the blend mode. (See `BlendMode` under [`enums.py`](/pxdlib/enums.py) for a list of values.)

<a id="color-adjustments"></a>
## Color adjustments

The `color-adjustments` key is a verlist (version 2). (unknown)

<a id="effects-data"></a>
## Effects data

The `effects-data` key is a verlist. (unknown)