# Pixelmator Pro (.pxd) format: Layer styles

Inside [`layer_info`](/docs/pxd/#sql), each layer may optionally have the keys [`styles-data`](#styles-data), [`color-adjustments`](#color-adjustments) and [`effects-data`](#effects-data) tables. (If present, the respective tool will be semi-highlighted in Pixelmator Pro).

All of the three are UTF-8 encoded JSON dictionaries. ([Structures](/docs/pxd/readme.md#json) such as 'vercon' and 'verlist' will crop up here.) They are as follows:

<a id="styles-data"></a>
## Styles data

The `styles-data` key is a verlist. (unknown)

<a id="color-adjustments"></a>
## Color adjustments

The `color-adjustments` key is a verlist (version 2). (unknown)

<a id="effects-data"></a>
## Effects data

The `effects-data` key is a verlist. (unknown)