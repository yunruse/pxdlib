'''
TextLayer object, bound to a PXD file.
'''

import json
import base64
import plistlib

from .structure import verb
from .layer import Layer
from .layer_text_style import TextStyle

from .plist import PlistFile, NSArray


class TextLayer(Layer):
    def _repr_info(self):
        if len(self.raw_text) > 20:
            yield f'{len(self.raw_text)} characters'
        else:
            yield repr(self.raw_text)
        if len(self.text_styles) > 1:
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
        store = self.__string_data()
        data = base64.b64decode(store['stringNSCodingData'])
        return PlistFile(plistlib.loads(data, fmt=plistlib.FMT_BINARY))

    @_text.setter
    def _text(self, val: PlistFile):
        data = plistlib.dumps(val._tree, fmt=plistlib.FMT_BINARY)
        data = base64.b64encode(data).decode()
        store = self.__string_data()
        store['stringNSCodingData'] = data
        self._setinfo('text-stringData', json.dumps([1, store]))

    @property
    def raw_text(self):
        '''
        Unformatted text contents.
        '''
        return self._text.NSString.value

    @raw_text.setter
    def raw_text(self, value: str):
        # TODO: Fix this -- it deletes layers
        raise NotImplementedError(
            'Cannot set raw_text currently.')
        _t = self._text
        _t.NSString.value = value
        self._text = _t
    
    @property
    def text_styles(self):
        attrs = self._text.NSAttributes
        if not isinstance(attrs, NSArray):
            attrs = [attrs]
        return [TextStyle(a) for a in attrs]