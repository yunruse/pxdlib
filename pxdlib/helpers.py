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


def BoundList(prop):
    '''
    A list that, when modified, re-sets its parent. Useful for convenience properties.
    '''
    class bindy(list):
        __slots__ = ('_BoundList__bind', )

        def _bind(self, val):
            self._BoundList__bind = val
            return self

        def _bind_update(self):
            setattr(self._BoundList__bind, prop, self)

        def append(self, obj):
            list.append(self, obj)
            self._bind_update()

        def clear(self):
            list.clear(self)
            self._bind_update()

        def extend(self, iterable):
            list.extend(self, iterable)
            self._bind_update()

        def insert(self, index: int, obj):
            list.insert(self, index, obj)
            self._bind_update()

        def pop(self, index: int):
            val = list.pop(self, index)
            self._bind_update()
            return val

        def remove(self, obj):
            list.remove(self, obj)
            self._bind_update()

        def reverse(self):
            list.reverse(self)
            self._bind_update()

        def sort(self, *, key, reverse=False):
            list.sort(self, key=key, reverse=reverse)
            self._bind_update()

    bindy.__name__ = f'<BoundList({prop!r})>'
    return bindy


def tupleBuddy(prop, names):
    '''
    Return a class mixin with convenient tuple accessors.
    For example, tupleBuddy('position', ('x', 'y'))
    makes .x and .y valid properties for .position.
    '''
    def wrapper(cls):
        assert prop.isidentifier()
        for i, n in enumerate(names):
            assert n.isidentifier()

            def getter(self):
                return getattr(self, prop)[i]

            def setter(self, val):
                vals = list(getattr(self, prop))
                vals[i] = val
                setattr(self, prop, tuple(vals))

            setattr(cls, n, property(
                getter, setter, doc=f'Convenience member for self.{prop}[{i}].'))
        return cls
    return wrapper


def synonymBuddy(aliases):
    def wrapper(cls):
        for link, aa in aliases.items():
            assert link.isidentifier(), link

            def getter(self):
                return getattr(self, link)

            def setter(self, val):
                setattr(self, link, val)

            prop = property(getter, setter)
            for a in aa:
                assert a.isidentifier(), a
                setattr(cls, a, prop)
        return cls
    return wrapper
