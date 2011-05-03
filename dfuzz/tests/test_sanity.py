#!/usr/bin/env python
import os
import shutil
import tempfile
import unittest

from dfuzz.core import sanity
from dfuzz.tests.dummy import sanity_cfg
from dfuzz.tests.dummy import sanity_cfg_validators as scv

class testFindBinary(unittest.TestCase):
    def setUp(self):
        self.binary = 'passwd'
        self.binary_path = os.path.join('/usr', 'bin')
        self.whole = os.path.join(self.binary_path, self.binary)

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

class testDirIntegrity(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.cfg = sanity_cfg.dummyCfg()
        self.cfg.work_dir = self.test_dir

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_dir_integrity_writable_wd(self):
        '''
        Test whether integrity fails if work_dir
        is not writable.
        '''
        os.chmod(self.test_dir, 0555)
        ret = sanity.dir_integrity(self.cfg)
        os.chmod(self.test_dir, 0777)
        self.assertEqual(ret, False)

    def test_dir_integrity_disable(self):
        '''
        Test whether modes get disabled if no matching
        input dir found.
        '''
        ret = sanity.dir_integrity(self.cfg)
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
        ret = sanity.dir_integrity(self.cfg)
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

        ret = sanity.dir_integrity(self.cfg)

        self.assertEqual(self.cfg.gen_dir, gen_abs)
        self.assertEqual(self.cfg.mut_dir, mut_abs)
        self.assertEqual(self.cfg.comb_dir, comb_abs)

        self.assertEqual(self.cfg.tmp_dir, tmp_abs)
        self.assertEqual(self.cfg.log_dir, log_abs)
        self.assertEqual(self.cfg.incidents_dir, inc_abs)

    def _change_perms(self, partial):
        '''
        Create `partial` subdir in self.test_dir directory,
        drop permissions and call dir_integrity.
        '''
        abs_path = os.path.join(self.test_dir, partial)
        os.mkdir(abs_path)
        os.chmod(abs_path, 0000)
        ret = sanity.dir_integrity(self.cfg)
        os.chmod(abs_path, 0777)

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

class testValidators(unittest.TestCase):
    def test_required(self):
        self.assertFalse(sanity.check_required(scv.empty()))
        self.assertFalse(sanity.check_required(scv.invalid()))
        self.assertTrue(sanity.check_required(scv.valid()))

if __name__ == "__main__":
    unittest.main()
