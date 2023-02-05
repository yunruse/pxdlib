# `pxdlib` API: Structures

Layers may hold various structures which provide information. 

Layers may hold or take a `Color` or `Gradient` object. They should be fairly explanatory, but they are documeted here just in case.

## Color
<a id="Color"></a>

A `Color` object represents a color in a variety of contexts. Calling `str` on it returns its 6- or 4-char hex value.

More specifically, it's a list of `[R, G, B, A]`, where all are integers from 0 through 255. You can instantiate it through a variety of methods:

## Gradient
<a id="Gradient"></a>

## Enums
<a id="Enums"></a>

Certain enumerables exist that may be used in functions or attributes. They are fairly self-documented in [enums.py](/pxdlib/enums.py).