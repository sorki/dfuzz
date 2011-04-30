import shlex
import logging
import subprocess

class Target(object):
    def __init__(self, cfg):
        self.cfg = cfg
        self.target = self.cfg.binary
        self.args = self.cfg.args

        self.stderr = ''
        self.stdout = ''
        self.code = 0

    def run(self, input_file):
        self.cmd = '%s %s' % (self.target,
            self.args % {'input': input_file})
        logging.debug('Running %s', self.cmd)

        # TODO (major): timeouts
        proc = subprocess.Popen(shlex.split(self.cmd),
            env={'LIBC_FATAL_STDERR_': '1'},
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        (self.stdout, self.stderr) = proc.communicate()
        self.retcode = proc.poll()
