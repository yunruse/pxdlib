# `pxdlib` API: Structures

Layers may hold various structures which provide information. 

Layers may hold or take a `Color` or `Gradient` object. They should be fairly explanatory, but they are documeted here just in case.

<a id="Color"></a>
## Color

A `Color` object represents a... well, a color. More specifically, it's a list of `[R, G, B, A]`, where all are integers from 0 through 255. You can instantiate it through a variety of methods:

<a id="Gradient"></a>
## Gradient

<a id="Enums"></a>
## Enums

Certain enumerables exist that may be used in functions or attributes. They are fairly self-documented in [enums.py](/pxdlib/enums.py).