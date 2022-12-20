'''
TextLayer object, bound to a PXD file.
'''

import json
import base64
import plistlib

from .structure import verb
from .layer import Layer

from .plist.plistfile import PlistFile


class TextLayer(Layer):
    @property
    def _text(self):
        store = verb(json.loads(self._info('text-stringData')))
        data = base64.b64decode(store['stringNSCodingData'])
        return PlistFile(plistlib.loads(data, fmt=plistlib.FMT_BINARY))

    @_text.setter
    def _text(self, val: PlistFile):
        store = verb(json.loads(self._info('text-stringData')))
        data = plistlib.dumps(val._tree, fmt=plistlib.FMT_BINARY)
        data = base64.b64encode(data).decode()
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