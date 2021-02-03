'''
Common functions used in pxdlib.
'''

from uuid import uuid1


def uuid():
    return str(uuid1()).upper()


def num(number):
    '''
    Return float (or int, if an integer)
    '''
    n = float(number)
    n_int = int(number)
    return n_int if n_int == n else n


def hexbyte(val):
    '''Turn a number to two hex digits.'''
    assert 0 <= val <= 255
    return hex(round(val))[2:].zfill(2)


def dicts(*dicts, **kwargs):
    '''
    Concatenate dictionaries such that defaults are on the left.

    Equivalent to | chaining in Python 3.9.
    '''
    result = dict()
    for d in dicts:
        result.update(d)
    result.update(kwargs)
    return result


def tupleBuddy(prop, names):
    '''
    Return a class mixin with convenient tuple accessors.
    For example, tupleBuddy('position', ('x', 'y'))
    makes .x and .y valid properties for .position.
    '''
    assert prop.isidentifier()
    for i in names:
        assert i.isidentifier()
    helper = type(f'{prop}Helper', (), {
        '__doc__': f'Auto-generated with: tupleBuddy({prop!r}, {names})'
    })
    for i, n in enumerate(names):
        def getter(self):
            return getattr(self, prop)[i]

        def setter(self, val):
            vals = list(getattr(self, prop))
            vals[i] = val
            setattr(self, prop, tuple(vals))

        setattr(helper, n, property(
            getter, setter, doc=f'Convenience member for self.{prop}[{i}].'))
    return helper


SizeHelper = tupleBuddy('size', ('width', 'height'))
PosHelper = tupleBuddy('position', ('x', 'y'))
