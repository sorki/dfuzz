import logging
import subprocess

class Target(object):
    def __init__(self, target, args=[]):
        self.target = target
        self.args = args

    def run(self, input_file):
        cmd = '%s %s' % (self.target,
            self.args % {'input': input_file})
        logging.debug('Running %s', cmd)

        proc = subprocess.Popen(cmd.split(' '),
            env={'LIBC_FATAL_STDERR_': '1'},
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        retcode = proc.wait()
        (stdout, stderr) = proc.communicate()
        logging.debug(retcode)
        logging.debug(stdout)
        logging.debug(stderr)
        if retcode != 0:
            pass
            # incident
