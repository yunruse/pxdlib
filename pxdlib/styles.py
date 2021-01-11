class Style(dict):
    _tag = None

    def __repr__(self):
        return f'{type(self).__name__}({dict.__repr__(self)})'

    @classmethod
    def _from_dict(cls, data):
        return cls(data)


class Fill(Style):
    _tag = 'f'


class Stroke(Style):
    _tag = 's'


class Shadow(Style):
    _tag = 'S'


class InnerShadow(Style):
    _tag = 'i'


_STYLES = {c._tag: c for c in (Fill, Stroke, Shadow, InnerShadow)}
