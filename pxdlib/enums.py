'''
Enumerables used in layer objects.
'''
import enum


class LayerFlag(enum.IntFlag):
    visible = 1 << 0
    locked = 1 << 1
    clipping = 1 << 3
    mask = 1 << 4
    raster = 1 << 6


class BlendMode(enum.Enum):
    passThrough = 'pass'
    normal = 'norm'
    darken = 'dark'
    multiply = 'mul '
    colorBurn = 'idiv'
    linearBurn = 'lbrn'
    darkerColor = 'dkCl'
    lighten = 'lite'
    screen = 'scrn'
    colorDodge = 'div '
    linearDodge = 'lddg'
    lighterColor = 'lgCl'
    overlay = 'over'
    softLight = 'sLit'
    hardLight = 'hLit'
    vividLight = 'vLit'
    linearLight = 'lLit'
    pinLight = 'pLit'
    hardMix = 'hMix'
    difference = 'diff'
    exclusion = 'smud'
    subtract = 'fmud'
    divide = 'fdiv'
    hue = 'hue '
    saturation = 'sat '
    color = 'colr'
    luminosity = 'lum '


class LayerTag(enum.IntEnum):
    none = 0
    red = 1
    orange = 2
    yellow = 3
    green = 4
    blue = 5
    purple = 6
    gray = 7
