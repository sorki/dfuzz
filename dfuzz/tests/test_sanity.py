#!/usr/bin/env python
import os
import shutil
import tempfile
import unittest

from dfuzz.core import sanity

class dummyCfg(object):
    def __init__(self):
        self.generation = True
        self.gen_dir = 'gen'
        self.mutation = True
        self.mut_dir = 'mut'
        self.combination = True
        self.comb_dir = 'comb'
        self.log_dir = 'log'
        self.incidents_dir = 'fails'
        self.tmp_dir = 'tmp'

class testSanity(unittest.TestCase):
    def setUp(self):
        self.binary = 'passwd'
        self.binary_path = os.path.join('/usr', 'bin')
        self.whole = os.path.join(self.binary_path, self.binary)

        self.test_dir = tempfile.mkdtemp()

        self.cfg = dummyCfg()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_find_binary_relative(self):
        '''
        Find binary - relative path
        '''
        ret = sanity.find_binary(self.binary, self.binary_path)
        self.assertEqual(ret, self.whole)

    def test_find_binary_absolute(self):
        '''
        Find binary - absolute path
        '''
        ret = sanity.find_binary(self.whole, '/home')
        self.assertEqual(ret, self.whole)

    def test_find_binary_path(self):
        '''
        Find binary - $PATH
        '''
        ret = sanity.find_binary(self.binary, '/home')
        self.assertEqual(ret, self.whole)

    def test_dir_integrity_writable_wd(self):
        '''
        Test whether integrity fails if work_dir
        is not writable.
        '''
        os.chmod(self.test_dir, 555)
        ret = sanity.dir_integrity(self.test_dir, object)
        os.chmod(self.test_dir, 777)
        self.assertEqual(ret, False)

    def test_dir_integrity_disable(self):
        '''
        Test whether modes get disabled if no matching
        input dir found.
        '''
        ret = sanity.dir_integrity(self.test_dir, self.cfg)
        self.assertEqual(self.cfg.generation, False)
        self.assertEqual(self.cfg.mutation, False)
        self.assertEqual(self.cfg.combination, False)

    def test_dir_integrity_enable(self):
        '''
        Test whether modes are enabled if there are
        input dirs.
        '''
        os.mkdir(os.path.join(self.test_dir, self.cfg.gen_dir))
        os.mkdir(os.path.join(self.test_dir, self.cfg.mut_dir))
        os.mkdir(os.path.join(self.test_dir, self.cfg.comb_dir))
        ret = sanity.dir_integrity(self.test_dir, self.cfg)
        self.assertEqual(self.cfg.generation, True)
        self.assertEqual(self.cfg.mutation, True)
        self.assertEqual(self.cfg.combination, True)

    def test_dir_integrity_abspath(self):
        '''
        Test absolute path updates in cfg object
        '''
        gen_abs = os.path.join(self.test_dir, self.cfg.gen_dir)
        mut_abs = os.path.join(self.test_dir, self.cfg.mut_dir)
        comb_abs = os.path.join(self.test_dir, self.cfg.comb_dir)

        tmp_abs = os.path.join(self.test_dir, self.cfg.tmp_dir)
        log_abs = os.path.join(self.test_dir, self.cfg.log_dir)
        inc_abs = os.path.join(self.test_dir, self.cfg.incidents_dir)

        os.mkdir(os.path.join(self.test_dir, self.cfg.gen_dir))
        os.mkdir(os.path.join(self.test_dir, self.cfg.mut_dir))
        os.mkdir(os.path.join(self.test_dir, self.cfg.comb_dir))

        ret = sanity.dir_integrity(self.test_dir, self.cfg)

        self.assertEqual(self.cfg.gen_dir, gen_abs)
        self.assertEqual(self.cfg.mut_dir, mut_abs)
        self.assertEqual(self.cfg.comb_dir, comb_abs)

        self.assertEqual(self.cfg.tmp_dir, tmp_abs)
        self.assertEqual(self.cfg.log_dir, log_abs)
        self.assertEqual(self.cfg.incidents_dir, inc_abs)

    def _change_perms(self, partial):
        abs_path = os.path.join(self.test_dir, partial)
        os.mkdir(abs_path)
        os.chmod(abs_path, 0)
        ret = sanity.dir_integrity(self.test_dir, self.cfg)
        os.chmod(abs_path, 777)

        return ret

    def test_dir_integrity_readable(self):
        for partial in [self.cfg.gen_dir, self.cfg.mut_dir,
            self.cfg.comb_dir]:

            ret = self._change_perms(partial)
            self.assertEqual(ret, False)

    def test_dir_integrity_writable_log(self):
        ret = self._change_perms(self.cfg.log_dir)
        self.assertEqual(ret, False)

    def test_dir_integrity_writable_inc(self):
        ret = self._change_perms(self.cfg.incidents_dir)
        self.assertEqual(ret, False)

if __name__ == "__main__":
    unittest.main()
