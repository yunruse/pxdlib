'''
Common functions used in pxdlib.
'''


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
