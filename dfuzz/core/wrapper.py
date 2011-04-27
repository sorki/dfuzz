import logging
import subprocess

from dfuzz.core import exceptions

class DfuzzWrapper(object):
    def __str__(self):
        return 'undefined wrapper, add __str__ method'

    def system(self, command):
        logging.debug('Executing: %s', command)
        pr = subprocess.Popen(command, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = pr.communicate()
        retcode = pr.poll()
        if retcode != 0:
            logging.error('Command "%s" returned nonzero value '
                'try running it by hand', command)
            raise exceptions.SyscallException(stdout, stderr)

        return stdout