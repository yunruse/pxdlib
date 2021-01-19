'''
Color adjustments with a wrapper to allow layer.adjusts.x.y = val.
'''

# Color adjustments are found using data[k1][k2]. As such,
# we construct a set of data structs to help facilitate this.

# this cruft gets added in too; purpose is not wholly deciphered
# but imagined to be color profiles
_DEFAULTS = {
    "e": 0,
    "E": 0,
    "V": 1,
    "csr": 0,
    "in": 1,
    "ctx": [1, {"cs": [1, {"map": {"0": [1, {"m": 2, "k": 0, "icc": "data"}]}}]}],
}
# {k1: data}
_KEYS = {
    "ca": [1, {"A": 0}],
    "r": [1, {"r": [1, {"r": 0.5, "i": 1}]}],
    "hS": [1, {"v": 0, "A": 0, "s": 0, "h": 0}],
    "s": [1, {"i": 1}],
    "f": [1, {"c": 0, "f": 1}],
    "g": [1, {"i": 0.5, "s": 0.25}],
    "L": [1, {}],
    "M": [1, {"i": 1, "c": [1, {"m": 2, "c": [0.592, 0.45, 0.305, 1], "csr": 0}]}],
    "v": [1, {"b": 0, "e": 0.5, "s": 1}],
    "i": [1, {"i": 1}],
    "w": [1, {"T": 0, "A": 0, "E": 1, "t": 0}],
    "cL": [1, {"a": 1}],
    "B": [1, {"E": 1, "A": 0}],
    "C": [2, {
        k: [1, {"d": 0, "p": [[0, 0], [1, 1]], "s": 0, "l": 0, "h": 0}]
        for k in ("rgb", "l", "r", "g", "b")
    }],
    "l": [1, {"c": 0, "h": 0, "E": 1, "A": 0, "B": 0, "e": 0, "s": 0, "b": 0}],
    "m": [1, {}],
    "S": [1, {"i": 0.5, "r": 2.5}],
    "b": [1, {"i": 1, "t": 0}]
}
for k, v in _KEYS.items():
    val = {"V": 1, "E": 0}
    val.update(v[1])
    _DEFAULTS[k] = [v[0], val]

# {k1: Adjustment}
_ADJUSTMENTS = {}
# each Adjustment._attribs is a {k2: funcname}

class ColorAdjustments:
    '''
    Color adjustments for a layer.

    This should be accessed directly from a layer;
    it is automatically created for one, and should
    not be created by the user.
    '''

    def __init__(self, layer, data):
        self._layer = layer
        if data is None:
            data = _DEFAULTS
        self._data = data

    def _update(self):
        # called whenever property is changed
        self._layer.adjusts = self

    def __repr__(self):
        changes = []
        for k1 in _KEYS:
            default = _DEFAULTS[k1]
            v = self._data[k1]
            if default == v:
                continue
            prop1 = _ADJUSTMENTS[k1]._name
            for k2, prop2 in _ADJUSTMENTS[k1]._attribs.items():
                val = v[1][k2]
                if val != default[1][k2]:
                    changes.append(f'  .{prop1}.{prop2} = {val}')
        if changes:
            string = '<ColorAdjustments: as listed below>\n'
            string += '\n'.join(changes)
            return string
        else:
            return '<ColorAdjustments: as default>'


def adjustment(key, name):
    '''
    wrapper to handle binding layer.adjusts.x
    '''
    def wrapper(cls):
        cls._key = key
        cls._name = name
        _ADJUSTMENTS[key] = cls

        def getter(self):
            return cls(self)

        def setter(self, val):
            raise TypeError(
                'Cannot define any layer.adjusts.x; try setting layer.adjusts.x.y instead'
            )

        setattr(ColorAdjustments, name, property(getter, setter))
        return cls
    return wrapper


class Adjustment:
    '''
    A generic color adjustment.
    '''

    _key = 'a'
    _name = 'adjustment'
    _attribs = {}  # data_key: property_name

    def __init__(self, adjust):
        self.adjust = adjust

    def __repr__(self):
        changes = []
        v = self.adjust._data[self._key]
        default = _DEFAULTS[self._key]

        for k2, prop2 in self._attribs.items():
            val = v[1][k2]
            if val != default[1][k2]:
                changes.append(f'  .{prop2} = {val}')

        name = type(self).__name__
        if changes:
            string = f'<{name}: as listed below>\n'
            string += '\n'.join('  ' + c for c in changes)
            return string
        else:
            return f'<{name}: as default>'

    def _get(self, k2):
        return self.adjust._data[self._key]

    def _set(self, k2, value, enable_effect=True):
        data = self.adjust._data
        ver, val = data[self._key]
        val[k2] = value
        if 'A' in val:
            # disable 'auto'
            val['A'] = 0
        if enable_effect:
            val['E'] = enable_effect
        data[self._key] = [ver, val]
        self.adjust._update()

    @property
    def enabled(self):
        '''
        Whether the adjustment is enabled.

        Changing a property automatically enables the entire adjustment.
        '''
        return self._get('E')

    @enabled.setter
    def enabled(self, val):
        self._set('E', bool(val))


class Intensity:
    @property
    def intensity(self):
        pass


@adjustment('w', 'white_balance')
class WhiteBalance(Adjustment):
    @property
    def temperature(self):
        return self._get('t')

    @temperature.setter
    def temperature(self, val):
        if not -1 <= val <= 1:
            raise ValueError('temperature must be in range -1 to +1')
        self._set('t', val)

    @property
    def tint(self):
        return self._get('T')

    @tint.setter
    def tint(self, val):
        if not -1 <= val <= 1:
            raise ValueError('tint must be in range -1 to +1')
        self._set('T', val)

    _attribs = {'t': 'temperature', 'T': 'tint'}