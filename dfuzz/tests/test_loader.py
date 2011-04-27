#!/usr/bin/env python
import unittest

from dfuzz.core import loader
from dfuzz.tests.dummy import incomplete_wrapper
from dfuzz.tests.dummy import complete_wrapper
from dfuzz.tests.dummy import standard_wrapper

class FuzzWraper(object):
    ''' 
    Dumb wrapper class used for testing
    '''
    pass

class testLoader(unittest.TestCase):
    def setUp(self):
        self.ml = loader.ModuleLoader()
        self.invalid = 'dfuzz.tests.dummy.invalid_wrapper'
        self.incomplete = 'dfuzz.tests.dummy.incomplete_wrapper'
        self.complete = 'dfuzz.tests.dummy.complete_wrapper'
        self.standard = 'dfuzz.tests.dummy.standard_wrapper'

        self.cls_incomplete = incomplete_wrapper.FuzzWrapper
        self.cls_complete = complete_wrapper.FuzzWrapper
        self.cls_standard = standard_wrapper.FuzzWrapper

    def _add_invalid(self, str_mods):
        self.ml.add_valid_modules(str_mods, 'high')
        self.ml.add_valid_modules(str_mods, 'low')

        self.assertEqual(self.ml.high_priority, [])
        self.assertEqual(self.ml.low_priority, [])

    def test_add_valid_non(self):
        '''
        Non-existent modules added
        '''
        self._add_invalid('invalid1;in.va.lid2;low')

    def test_add_valid_miss(self):
        '''
        Existing modules added, missing required class
        '''
        self._add_invalid('sys;os;unittest;subprocess')

    def test_add_valid_invalid(self):
        '''
        Existing module, empty class
        '''
        self._add_invalid(self.invalid)


    def test_add_valid_incomplete(self):
        '''
        Existing module, emtpy class
        '''
        self._add_invalid(self.incomplete)

    def test_add_valid_valid(self):
        '''
        Valid modules
        '''
        self.ml.add_valid_modules(self.complete, 'high')
        self.ml.add_valid_modules(self.standard, 'low')

        self.assertEqual(self.ml.high_priority,
            [(self.cls_complete, [])])
        self.assertEqual(self.ml.low_priority,
            [(self.cls_standard, [])])

    def test_add_valid_params(self):
        '''
        Valid modules + paramaters
        '''
        self.ml.add_valid_modules(self.complete+'(param1, 1)', 'high')
        self.ml.add_valid_modules(self.standard+'(a,2,3)', 'low')

        self.assertEqual(self.ml.high_priority,
            [(self.cls_complete, ['param1', '1'])])
        self.assertEqual(self.ml.low_priority,
            [(self.cls_standard, ['a', '2', '3'])])

    def test_add_valid_complex(self):
        '''
        Complex input
        '''
        inp = ('sys; %s(param1, 1); os ; %s(a,2,3) ;' %
            (self.complete, self.standard))
        self.ml.add_valid_modules(inp, 'high')

        self.assertEqual(self.ml.high_priority,
            [(self.cls_complete, ['param1', '1']),
             (self.cls_standard, ['a', '2', '3'])])


    def test_validate_module(self):
        '''
        Module validation (required class name + methods)
        '''
        self.assertEqual(self.ml.validate_module('sys'), False)
        self.assertEqual(self.ml.validate_module('no_such'), False)
        self.assertEqual(self.ml.validate_module(self.invalid), False)
        self.assertEqual(self.ml.validate_module(self.incomplete), False)
        self.assertEqual(self.ml.validate_module(self.complete),
            self.cls_complete)
        self.assertEqual(self.ml.validate_module(self.standard),
            self.cls_standard)

    def test_check_methods(self):
        '''
        Required methods checking
        '''
        ret = self.ml.check_methods(self.cls_incomplete, '')
        self.assertFalse(ret)
        ret = self.ml.check_methods(self.cls_complete, '')
        self.assertTrue(ret)
        ret = self.ml.check_methods(self.cls_standard, '')
        self.assertTrue(ret)


if __name__ == "__main__":
    unittest.main()
