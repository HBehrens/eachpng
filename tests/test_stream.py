import unittest
import mock
from eachpng import eachpng
from io import BytesIO


class StreamTest(unittest.TestCase):

    def test_empty(self):
        cb = mock.Mock()
        eachpng.handle_stream(BytesIO(), cb)
        cb.assert_not_called()


    def test_no_png(self):
        cb = mock.Mock()
        eachpng.handle_stream(BytesIO(eachpng.PNG_START), cb)
        cb.assert_not_called()


    def test_single_png(self):
        cb = mock.Mock()
        eachpng.handle_stream(BytesIO(b'pre' + eachpng.PNG_START + b'someContent' + eachpng.PNG_END + b'post'), cb)
        cb.assert_called_once_with(eachpng.PNG_START + b'someContent' + eachpng.PNG_END)

    def test_multiple_png(self):
        cb = mock.Mock()
        eachpng.handle_stream(BytesIO(
            b'pre' + eachpng.PNG_START + b'content1' + eachpng.PNG_END + b'mid' +
                     eachpng.PNG_START + b'content2' + eachpng.PNG_END + b'end'), cb)

        cb.assert_has_calls([
            mock.call(eachpng.PNG_START + b'content1' + eachpng.PNG_END),
            mock.call(eachpng.PNG_START + b'content2' + eachpng.PNG_END)])
