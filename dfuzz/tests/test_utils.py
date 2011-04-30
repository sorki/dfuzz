import unittest

from dfuzz.core import utils
from dfuzz.core import loader

class testUtils(unittest.TestCase):
    def test_parse_args_empty(self):
        ret = utils.parse_args('')
        self.assertEqual(ret, '')

    def test_parse_args_def(self):
        ret = utils.parse_args('FUZZED_FILE')
        self.assertEqual(ret, '%(input)s')

    def test_parse_args(self):
        ret = utils.parse_args('str -option -s --long=FUZZED_FILE')
        self.assertEqual(ret, 'str -option -s --long=%(input)s')

    def test_parse_args2(self):
        ret = utils.parse_args('str -option A -option B C',
            mapping={'str': 'nostr', 'A': 'X', 'B': 'Y', 'C': 'Z'})
        self.assertEqual(ret, 'nostr -option X -option Y Z')


    def test_get_class(self):
        fn = utils.get_class_by_path
        self.assertFalse(fn('no.such.module'))
        self.assertFalse(fn('sys.NoSuchClass'))
        self.assertEqual(loader.ModuleLoader,
            fn('dfuzz.core.loader.ModuleLoader'))
if __name__ == "__main__":
    unittest.main()
