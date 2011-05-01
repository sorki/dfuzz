#!/usr/bin/env python
import os
import unittest

import dfuzz
from dfuzz.core import conf

class testConf(unittest.TestCase):
    def setUp(self):
        def_path = os.path.join(
            os.path.dirname(dfuzz.__file__), 'cfg')
        self.c = conf.Config(def_path, 'defaults.ini')
        self.attr = 'timeout'

    def test_init(self):
        pass

    def test_attrs(self):
        self.assertTrue(hasattr(self.c, self.attr))

    def test_as_dict(self):
        self.assertEqual(
            self.c.as_dict()[self.attr],
            getattr(self.c, self.attr))

    def test_dict_update(self):
        setattr(self.c, self.attr, 'new')
        self.assertEqual(
            self.c.as_dict()[self.attr],
            getattr(self.c, self.attr))

if __name__ == "__main__":
    unittest.main()
