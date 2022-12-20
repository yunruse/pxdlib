'''
TextLayer object, bound to a PXD file.
'''

import json
import base64
import plistlib

from .structure import verb
from .layer import Layer


class TextLayer(Layer):
    @property
    def _text(self):
        store = verb(json.loads(self._info('text-stringData')))
        data = base64.b64decode(store['stringNSCodingData'])
        return plistlib.loads(data, fmt=plistlib.FMT_BINARY)

    @_text.setter
    def _text(self, val):
        store = verb(json.loads(self._info('text-stringData')))
        data = plistlib.dumps(val, fmt=plistlib.FMT_BINARY)
        data = base64.b64encode(data).decode()
        store['stringNSCodingData'] = data
        self._setinfo('text-stringData', json.dumps([1, store]))

    @property
    def rawText(self):
        '''
        Raw, unformatted text contents.
        '''
        _t = self._text
        o = _t['$objects']
        return o[o[1]['NSString']]['NS.string']

    @rawText.setter
    def _rawText(self, val):
        # currently doesn't work and just deletes layer
        _t = self._text
        o = _t['$objects']
        o[o[1]['NSString']]['NS.string'] = val
        self._text = _t