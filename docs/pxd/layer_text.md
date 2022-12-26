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

### `NSAttributeInfo` (run-length encoding for text styles)

`NSAttributeInfo` (if present) is an `NSMutableData` providing an run-length encoding. In order, it interleaves the number of characters, then those characters' style index, and so on. For example:

- The string `001110000` is encoded by [2 0 3 1 4 0]
- The string `000011` followed by 257 `2`s is encoded as [4 0  2 1 129 2 2], where [129 2] decodes to 257 (see below).

Encoders should take care to avoid reading from indices

#### 7-bit arbitrary-length integer format

In this run-length encoding, numbers are presented with a simple 7-bit format. This means numbers can be of an arbitrary byte length, and should be serially decoded.

The most significant bit indicates if it is not the final byte of the number; the remaining 7 bits are the number. The resultant 7-bit chunks are in reverse order such that the most significant 7-bit chunk comes first.

For example, numbers may be encoded as:

```
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
- The string `001110000` is encoded by [2 0 3 1 4 0]
- The string `000011` followed by 257 `2`s is encoded as [4 0  2 1 129 2 2], where [129 2] decodes to 257.


## `NSAttributes` (text styles)

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
- `font-style-data` is a JSON-encoded UTF-8 vercon with the following properties:
  - `s` (`number`): The font size (also in `NSFontSizeAttribute` below!)
  - `n` (`str`): The font (also in `NSFontNameAttribute` below!)
  - `b` (`number`): 1 iff bold.
  - `i` (`number`): 1 iff italic.


- `color` is an `NSDict`. It has the following keys:
  - `NSRGB` (`bytes`): The color in RGBA. Space-separated floats (ASCII) suffixed with a null byte.
  - `NSComponents` (`bytes`): The color in RGBA, as rendered in the color space (and as reported by Pixelmator). Space-separated floats (ASCII).
  - `NSColorSpace` (`int`): Default 1 (IEC 61966-2.1).
  - `NSCustomColorSpace`: The colorspace. See [Apple's guide](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/DrawColor/Tasks/UsingColorSpaces.html#//apple_ref/doc/uid/TP40001807) for more information.
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