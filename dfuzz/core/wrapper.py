import logging
import subprocess

from dfuzz.core import exceptions

class DfuzzWrapper(object):
    ''' 
    Abstract class to be used as base for
    new wrappers or standalone fuzzers
    '''

    def __str__(self):
        '''
        New class should override this method.
        Provides easy identification.
        '''
        return 'undefined wrapper, add __str__ method'

    def system(self, command):
        '''
        Safely executes supplied command.
        If the return code of the command is zero, it will
        return the output of the command.

        Raises SyscallException in case of nonzero return code.
        '''
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
