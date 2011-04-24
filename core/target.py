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

        #subprocess.
