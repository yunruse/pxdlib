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
    '''
    The blend mode for a layer or style.

    (The string value is the encoded string used for layers.)
    '''
    # All strings used correspond to the layer's blend modes.
    passThrough = 'pass'
    normal = 'norm'

    # The keys listed below are that which can be applied to styles.
    sourceOver = 'norm'
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


class FillType(enum.IntEnum):
    color = 0
    gradient = 1


class GradientType(enum.IntEnum):
    linear = 0
    radial = 1
    angle = 2


class StrokeType(enum.IntEnum):
    regular = 0
    dashed = 1
    dotted = 2


class StrokePosition(enum.IntEnum):
    inside = 0
    center = 1
    outside = 2
