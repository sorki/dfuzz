#!/usr/bin/env python
import logging
import unittest

import test_conf
import test_utils
import test_sanity
import test_loader
import test_incident

def get_suite():
    logging.disable(logging.CRITICAL)
    ts = unittest.TestSuite()
    loader = unittest.TestLoader()
    classes = [
        test_sanity.testFindBinary,
        test_sanity.testDirIntegrity,
        test_sanity.testValidators,
        test_loader.testLoader,
        test_conf.testConf,
        test_utils.testUtils,
        test_incident.testIncident]

    for cls in classes:
        ts.addTest(loader.loadTestsFromTestCase(cls))

    return ts


def main():
    logging.disable(logging.CRITICAL)
    unittest.TextTestRunner().run(get_suite())

if __name__ == "__main__":
    main()
