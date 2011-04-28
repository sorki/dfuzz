import shlex
import logging
import subprocess

class Target(object):
    def __init__(self, target, args=[]):
        self.target = target
        self.args = args

        self.stderr = ''
        self.stdout = ''
        self.code = 0

    def run(self, input_file):
        cmd = '%s %s' % (self.target,
            self.args % {'input': input_file})
        logging.debug('Running %s', cmd)

        proc = subprocess.Popen(shlex.split(cmd),
            env={'LIBC_FATAL_STDERR_': '1'},
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        (self.stdout, self.stderr) = proc.communicate()
        self.retcode = proc.poll()
