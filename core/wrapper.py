import logging
import subprocess

class SyscallException(Exception):
    def __init__(self, stdout, stderr):
        self.stdout = stdout
        self.stderr = stderr

        self.line = '-'*20
        self.str_stdout = 'stdout'.center(20, '-')
        self.str_stderr = 'stderr'.center(20, '-')

    def __str__(self):
        fmt = '\n%s\n\n%s\n%s\n'
        return (fmt % (self.str_stdout, self.stdout, self.line) +
            fmt % (self.str_stderr, self.stderr, self.line))

class DfuzzWrapper(object):
    def __str__(self):
        return 'undefined wrapper, add __str__ method'

    def system(self, command):
        logging.debug('Executing: %s' % command)
        pr = subprocess.Popen(command, shell=True, 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        retcode = pr.wait()
        (stdout, stderr) = pr.communicate()
        if retcode != 0:
            logging.error('Command "%s" returned nonzero value '
                'try running it by hand', command)
            raise SyscallException(stdout, stderr)

        return stdout
