# Pixelmator Pro (.pxd) format: Text layer styles

In [text layers](/docs/pxd/layer.md#text), the layer info tag `text-stringData` contains a single entry: `StringNSCodingData`, a base-64 encoded binary PLIST, in which most of the text data is stored.

## Note on PLIST formatting

As with all PLISTs, objects are stored under the `$objects` key, with a UID stored whenever an object is referenced. The internal `pxdlib.plist` library partially abstracts these details away by presenting structures that operate in a more Pythonic nature corresponding to the object type.

In general, many objects will have a `$class` key, indicating their nature. Take note of some primitives, with obviously-named properties:
- `NSString` and `NSMutableString` (`str`), with `NS.string`
- `NSData` and `NSMutableData` (`bytes`), with `NS.data`
- `NSArray` (`list`), with `NS.objects`
- `NSDictionary` (`dict`), with `NS.keys` and `NS.objects`

## `StringNSCodingData` root structure

The root element of this PLIST is an [`NSMutableAttributedString`](https://developer.apple.com/documentation/foundation/nsmutableattributedstring) representing the text element. It is comprised of two or three parts.

`NSString` is an `NSMutableString`, the raw text onto which formatting is applied.

If the text is of a single style, `NSAttribute` is an `NSDict` (see below for details). If the text has *multiple* styles, `NSAttribute` is an `NSArray` of the styles.

`NSAttributeInfo` is present only if there are multiple styles, providing the indexing for applying them. It is an `NSMutableData` that must be read serially. In general, _pop_ the number of characters, and then _pop_ the *style index* (from the `NSAttributes` array) that these characters apply unto.

For simple examples, _pop_ here is just reading a single byte. For example, the string `aabbbaaaa` - where `a` has style 0 and `b` style 1 - would result in the sequence of bytes [2, 0, 3, 1, 4, 0]. In the case that a number (style index or character count) is large enough, _pop_ takes a slightly different form. ???


## `NSAttributes`

The `NSAttributes` property is an `NSDict` (or list thereof) with a variety of properties, all of which are prepended with `com.pixelmatorteam.textkit.attribute.`, and:

- `glyph-info` seems to always be an empty string.
- `pixel-stroke` seems to always be 0.
- `outline-appearance` seems to always be 0.
- `character-spacing` (`float`): Integer-valued character spacing in percentage, -100 to 100.
- `baseline-offset` (`float`): Integer-valued baseline offset from -127 to +127.
- `underline` (`int`): Boolean for underline.
- `strikethrough` (`int`): Boolean for strikethrough.
- `capitalization` (`int`): 0 for no capitalisation, 1 for allcaps, 4 for start-case.
- `baseline` (`int`): 0 for regular text, 1 for superscript, -1 for subscript
- `ligature` (`int`): 0 to use no ligatures, 1 to use default ligatures, 2 to use all ligatures.

- `font-scale` (`int`): seems always to be 1 ???
- `font-style-data` is a JSON-encoded UTF-8 vercon with `{"s": x}` where `x` is the font size. This is duplicated ???
- `color` is an `NSDict`. It has the following keys:
  - `NSComponents`: ???
  - `NSRGB`: ???
  - `NSColorSpace` (`int`): Default 1.
  - `NSCustomColorSpace`: A colorspace (left as an exercise to the reader).
- `paragraph-style`: see below
- `font`: see below


### `com.pixelmatorteam.textkit.attribute.paragraph-style`

This is an `NSMutableParagraphStyle`.
It always has the following properties:
- `NSTextLists` ???
- `NSTextBlocks` ???
- `NSDefaultTabInterval` ???
- `NSWritingDirection` ???
- `NSTabStops` ???

It may optionally have the following properties:
- `NSFirstLineHeadIndent`, `NSHeadIndent` and `NSTailIndent` (`float`, default `0.0`): Integer number of pixels for *Indents* option under *First*, *Left* and *Right*. This provides horizontal padding to the document. `NSTailIndent` is always below 0; the others above.
- `NSLineHeightMultiple` (`float`, default `1.0`): The line height.
- `NSParagraphSpacing` and `NSParagraphSpacingBefore` (`float`, default `1.0`): the *Before Paragraph* and *After Paragraph* spacing, respectively.
- `NSAlignment` (`int`, default `0`): The horizontal alignment. 0 for left-aligned, 1 right-aligned, 2 centre-aligned, 3 justified


### `com.pixelmatorteam.textkit.attribute.font`

This is an `NSFontDescriptor`. It has two properties:
- `NSFontDescriptorOptions` (`int`): Nominally `1 << 31`. May have other properties ???
- `NSFontDescriptorAttributes`, an `NSDict` with keys:
  - `NSFontSizeAttribute` (`float`): The current font size
  - `NSFontFamilyAttribute`: The font name (eg `Helvetica`)
  - `NSFontFaceAttribute`: The font name (eg `Oblique`)
  - `NSFontNameAttribute`: The font name (eg `Helvetica-Oblique`)
  - `NSCTFontTraitsAttribute`: an object with the single attribute `NSCTFontSymbolicTrait`, nominally identical to `NSFontDescriptorOptions`.