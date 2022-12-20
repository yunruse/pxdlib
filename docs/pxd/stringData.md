# Pixelmator Pro (.pxd) format: Text layer styles

In [text layers](/docs/pxd/layer.md#text), the layer info tag `text-stringData` contains a single entry: `StringNSCodingData`, a base-64 encoded binary PLIST, in which most of the text data is stored.

## Note on PLIST formatting

As with all PLISTs, objects are stored under the `$objects` key, with a UID stored whenever an object is referenced. The internal `pxdlib.plist` library partially abstracts these details away by presenting structures that operate in a more Pythonic nature corresponding to the object type.

In general, many objects will have a `$class` key, indicating their nature. Take note of some primitives, with obviously-named properties:
- `NSString` and `NSMutableString` (`str`), with `NS.string`
- `NSData` and `NSMutableData` (`bytes`), with `NS.data`
- `NSArray` (`list`), with `NS.objects`
- `NSDictionary` (`dict`), with `NS.keys` and `NS.objects`

## Pixelmator's `NSMutableAttributedString` root structure

The root element of this PLIST is an [`NSMutableAttributedString`](https://developer.apple.com/documentation/foundation/nsmutableattributedstring) representing the text element, albeit a bit modified for Pixelmator's own purposes.

This contains, in and of itself, three properties:

- `NSString` is an `NSMutableString`, the raw text onto which formatting is applied.
- `NSAttributeInfo` is present iff text has multiple styles. It is a run-length encoded list of styles for each character. See below for details.
- `NSAttribute` is an `NSDict` with text style, OR a list of `NSDict` iff the text has multiple styles. See below for details.

### NSAttributeInfo

`NSAttributeInfo` (if present) is a run-length encoding. It is an `NSMutableData` that must be read serially. In general, _pop_ the number of characters, and then _pop_ the *style index* (from the `NSAttributes` array) that these characters apply unto.

This _pop_ encodes arbitrarily large numbers in an intriguing multi-byte method reminiscent of UTF-8 - hence why it is serially encoded and cannot be randomly-accessed.

If the byte's most significant bit is 0, it is the last byte; the next 7 bits encode the number. If the byte's MSB is 1, it is not the last byte. These 7-bit chunks are in reverse order (the smallest chunk is the smallest 7 bits). For example:

```
#number           pop format, binary
      3                     00000011
    128            10000000 00000001
    129            10000001 00000001
    256            10000000 00000010
    516            10000100 00000100
  16772   10000100 10000011 00000001
#                4        3        1
# 16772 = 4 + 3x + 1x^2 where x = 128
```

For completeness, here are some examples where a digit is styled according to its index (ie `a` has style 0, `b` style 1, etc):
- The string `001110000` results in [2 0 3 1 4 0]
- The string `000011` followed by 257 `2`s results in [4 0  2 1 129 2 2], where [129 2] decodes to 257.

(If you want to know how I generated text with more than 128 different styles to test that _pop_ works on style index as well as run-length, a bit of RTF hacking gives us [this image](https://cdn.discordapp.com/attachments/1054061996695367811/1054771575137783859/Screenshot_2022-12-20_at_2.45.29_pm.png) which roughly describes my thoughts on this whole shebang.)


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