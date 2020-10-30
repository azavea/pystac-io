import unittest

import pystac
import pystac_io
import pystac_io.s3


class TestPyStacIoContextManager(unittest.TestCase):
    def test_context_manager(self):
        from pystac_io.s3 import s3_read_text_method

        self.assertEqual(
            pystac.STAC_IO.read_text_method, pystac.STAC_IO.default_read_text_method
        )
        with pystac_io.register("s3"):
            self.assertEqual(pystac.STAC_IO.read_text_method, s3_read_text_method)
        self.assertEqual(
            pystac.STAC_IO.read_text_method, pystac.STAC_IO.default_read_text_method
        )

    def test_func_call(self):
        from pystac_io.s3 import s3_read_text_method

        self.assertEqual(
            pystac.STAC_IO.read_text_method, pystac.STAC_IO.default_read_text_method
        )

        pystac_io.register("s3")
        self.assertEqual(pystac.STAC_IO.read_text_method, s3_read_text_method)

        pystac_io.unregister()
        self.assertEqual(
            pystac.STAC_IO.read_text_method, pystac.STAC_IO.default_read_text_method
        )
