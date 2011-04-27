#!/usr/bin/env python
import logging
import unittest

import test_sanity

def get_suite():
    logging.disable(logging.CRITICAL)
    ts = unittest.TestSuite()
    loader = unittest.TestLoader()
    classes = [test_sanity.testSanity,]

    for cls in classes:
        ts.addTest(loader.loadTestsFromTestCase(cls))

    return ts


def main():
    logging.disable(logging.CRITICAL)
    unittest.TextTestRunner().run(get_suite())

if __name__ == "__main__":
    main()
