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


class SizeHelper:
    @property
    def width(self):
        return self.size[0]

    @width.setter
    def width(self, val):
        self.size = (val, self.height)

    @property
    def height(self):
        return self.size[1]

    @height.setter
    def height(self, val):
        self.size = (self.width, val)
