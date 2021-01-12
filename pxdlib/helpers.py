'''
Common functions used in pxdlib.
'''


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


def dirs(obj):
    '''
    Iterator of name, value for dir(obj).
    '''
    for k in dir(obj):
        yield k, getattr(obj, k)


def reversegetattr(obj, value, default=None):
    '''
    Get key such that object.key = value.
    '''
    for k, v in dirs(obj):
        if v == value:
            return k
    return None
