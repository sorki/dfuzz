#!/usr/bin/env python
import unittest

from dfuzz.core import incident
from dfuzz.tests.dummy import incident_required

class testIncident(unittest.TestCase):
    def setUp(self):
        self.dc = incident_required.Config()
        self.dt = incident_required.TargetObj()
        self.dh_class = incident_required.Handler
        self.fuzzer = 'test'

        self.i = incident.Incident(self.dc, self.fuzzer,
            self.dh_class)

    def test_defaults(self):
        '''
        Test whether the defaults are assigned
        '''
        self.assertEqual(self.i.crash_signals, [4, 6, 7, 8, 11])

    def test_set_list(self):
        '''
        Test list setter
        '''
        self.i.crash_signals = [1,2,9]
        self.assertEqual(self.i.crash_signals, [1,2,9])

    def test_set_string(self):
        '''
        Test string setter
        '''
        self.i.crash_signals = 'SIGILL SIGABRT'
        self.assertEqual(self.i.crash_signals, [4, 6])

        self.i.crash_signals = 'SIGILL, SIGABRT'
        self.assertEqual(self.i.crash_signals, [4, 6])

    def test_serious(self):
        '''
        Test singal (return code) catching
        '''
        sigs = range(10)
        self.i.crash_signals = sigs
        for s in sigs:
            self.assertTrue(self.i.serious(-s))

        nosigs = range(15, 20)
        for ns in nosigs:
            self.assertFalse(self.i.serious(-ns))

    def test_check(self):
        p = '/EL_PATH'
        self.i.check(self.dt, p)

if __name__ == "__main__":
    unittest.main()
