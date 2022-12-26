'''
TextLayer object, bound to a PXD file.
'''

import json

from .helpers import chunk
from .structure import arbint, verb

from .layer import Layer
from .layer_text_style import TextStyle

from .plist import PlistFile, NSArray

FormattedText = list[tuple[str, TextStyle]]

class TextLayer(Layer):
    def to_rich(self):
        text = ''
        for string, style in self.text:
            s = style.to_rich()
            text += f'[{s}]{string}[/]'
        return text

    def print(self):
        try:
            from rich import print as rich_print
        except ImportError:
            print(self.raw_text)
        else:
            rich_print(self.to_rich())

    def _repr_info(self):
        if len(self.raw_text) > 20:
            yield f'{len(self.raw_text)} characters'
        else:
            yield repr(self.raw_text)
        if self._multiple_styles():
            yield 'multiple text styles'
        else:
            yield from self.text_styles[0]._repr_info()
        yield from Layer._repr_info(self)
    
    def __string_data(self) -> dict:
        js = self._info('text-stringData')
        assert js, "No text-stringData!"
        return verb(json.loads(js))

    @property
    def _text(self):
        return PlistFile.from_base64(
            self.__string_data()['stringNSCodingData'])

    @_text.setter
    def _text(self, plist: PlistFile):
        store = self.__string_data()
        store['stringNSCodingData'] = plist.to_base64()
        self._setinfo('text-stringData', json.dumps([1, store]))
    
    # Text style (read)

    def _multiple_styles(self):
        return isinstance(self._text.NSAttributes, NSArray)

    @property
    def raw_text(self):
        '''Unformatted text contents.'''
        return self._text.NSString.value

    @property
    def _text_styles(self):
        '''Styles in use (by index).'''
        attrs = self._text.NSAttributes
        if not isinstance(attrs, NSArray):
            attrs = [attrs]
        return [TextStyle(a) for a in attrs]

    @property
    def text(self) -> FormattedText:
        text = self.raw_text
        style_index = self._text_styles
        if not hasattr(self._text, 'NSAttributeInfo'):
            assert len(style_index) == 1, \
                "Multiple styles but no NSAttributeInfo!"
            return [(text, style_index[0])]

            
        style_rle = arbint(self._text.NSAttributeInfo)

        n_text = 0
        styles: FormattedText = []
        for (n, i) in chunk(style_rle, 2):
            styles.append(
                (text[n_text:n_text+n], style_index[i]))
            n_text += n
        assert n_text == len(text)
        return styles


    # Text style (write)


    @raw_text.setter
    def raw_text(self, value: str):
        if not isinstance(value, str):
            raise TypeError('Text must be a string')
        
        if self._multiple_styles():
            # TODO: Only use first style
            raise AttributeError(
                'Cannot currently set raw_text.')
        _t = self._text
        _t.NSString.value = value
        self._text = _t

    @text.setter
    def text(self, value: FormattedText):
        raise AttributeError(
            'Cannot set currently set text.')