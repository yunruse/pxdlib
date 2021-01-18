
_DEFAULTS = {
    "e": 0,
    "E": 0,
    "V": 1,
    "csr": 0,
    "in": 1,
    "ctx": [1, {"cs": [1, {"map": {"0": [1, {"m": 2, "k": 0, "icc": "data"}]}}]}],
    "ca": [1, {"V": 1, "E": 0, "A": 0}],
    "r": [1, {"V": 1, "E": 0, "r": [1, {"r": 0.5, "i": 1}]}],
    "hS": [1, {"V": 1, "v": 0, "A": 0, "s": 0, "E": 0, "h": 0}],
    "s": [1, {"V": 1, "E": 0, "i": 1}],
    "f": [1, {"V": 1, "c": 0, "E": 0, "f": 1}],
    "g": [1, {"V": 1, "i": 0.5, "s": 0.25, "E": 0}],
    "L": [1, {"V": 1, "E": 0}],
    "M": [1, {"V": 1, "i": 1, "c": [1, {"m": 2, "c": [0.592, 0.45, 0.305, 1], "csr": 0}], "E": 0}],
    "v": [1, {"V": 1, "b": 0, "e": 0.5, "s": 1, "E": 0}],
    "i": [1, {"V": 1, "E": 0, "i": 1}],
    "w": [1, {"V": 1, "T": 0, "A": 0, "E": 1, "t": 0}],
    "cL": [1, {"V": 1, "E": 0, "a": 1}],
    "B": [1, {"V": 1, "E": 1, "A": 0}],
    "C": [2, {
        k: [1, {"d": 0, "p": [[0, 0], [1, 1]], "s": 0, "l": 0, "h": 0}]
        for k in ("rgb", "l", "r", "g", "b")
    }],
    "l": [1, {"V": 1, "c": 0, "h": 0, "E": 1, "A": 0, "B": 0, "e": 0, "s": 0, "b": 0}],
    "m": [1, {"V": 1, "E": 0}],
    "S": [1, {"V": 1, "i": 0.5, "r": 2.5, "E": 0}],
    "b": [1, {"V": 1, "i": 1, "E": 0, "t": 0}]
}


class ColorAdjustment:
    '''
    A generic color adjustment.
    '''

    def __init__(self, layer):
        self.layer = layer

    def _set(self, k1, k2, value):
        pass


class Intensity:
    @property
    def intensity(self):
        pass


class ColorAdjustments:
    '''
    Color adjustments for a layer.

    This should be accessed directly from a layer;
    it is automatically created for one, and should
    not be created by the user.
    '''

    def __init__(self, layer, data):
        self.layer = layer
        if data is None:
            data = _DEFAULTS
        self.data = data

    def __repr__(self):
        changes = []
        if changes:
            pass
        else:
            changes = "no changes from default"
        return f'<ColorAdjustments: {changes}>'
