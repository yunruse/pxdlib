class PixelmatorError(Exception):
    '''
    Some change was made which is invalid
    in a Pixelmator document.
    '''


class VersionError(PixelmatorError):
    '''
    Data structure at unexpected version.
    Most likely due to newer Pixelmator version existing.
    If you see this, try updating `pxdlib`.
    If it continues, contact the developer.
    '''


class ChildError(PixelmatorError):
    '''
    Attempted move of a layer to a parent layer
    for which an invalid error would occur.
    '''


class MaskError(ChildError):
    '''
    A layer was moved about in a way that creates
    a situation where a layer has a mask (but shouldn't)
    '''


class StyleError(PixelmatorError):
    '''
    An invalid style was set.
    '''
