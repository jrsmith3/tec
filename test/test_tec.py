# -*- coding: utf-8 -*-
import tec
import unittest

class AttributeExistence(unittest.TestCase):
    """
    Tests existence of specified attributes
    """
    def test_version(self):
        """
        tec.__version__ should exist
        """
        try:
            tec.__version__
        except AttributeError:
            self.fail("`tec` has no `__version__` attribute")
