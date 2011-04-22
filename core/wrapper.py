import logging
import subprocess

class DfuzzWrapper(object):
    def __str__(self):
        return 'undefined wrapper, add __str__ method'

    def system(self, command):
        print 'EXEC: %s' % command
        retcode = subprocess.call(command, shell=True)
        if retcode != 0:
            logging.error('Command "%s" returns nonzero value '
                'try running it by hand')
