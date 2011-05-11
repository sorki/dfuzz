import shlex
import logging
import threading
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

        self._proc = subprocess.Popen(shlex.split(self.cmd),
            env={'LIBC_FATAL_STDERR_': '1'},
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        (self.stdout, self.stderr) = self._proc.communicate()
        self.code = self._proc.poll()

class TimedTarget(Target):
    def alarm_handler(self):
        self._proc.kill()

    def run(self, input_file):
        timer = threading.Timer(int(self.cfg.timeout),
            self.alarm_handler)
        timer.start()

        super(TimedTarget, self).run(input_file)

        timer.cancel()

class TimedValgrindTarget(TimedTarget):
    def run(self, input_file):
        # normal run
        super(TimedValgrindTarget, self).run(input_file)
        nstdout = self.stdout
        nstderr = self.stderr
        ncode = self.code
        ncmd = self.cmd
        ntarget = self.target

        # valgrind run
        self.target = '%s %s' % ('valgrind --error-exitcode=101',
            self.target)

        super(TimedValgrindTarget, self).run(input_file)

        self.vgrind = self.stderr
        self.vgrind_cmd = self.cmd

        if not self.code == 101:
            self.code = ncode
        else:
            self.code = -101

        self.stdout = nstdout
        self.stderr = nstderr
        self.target = ntarget
        self.cmd = ncmd
