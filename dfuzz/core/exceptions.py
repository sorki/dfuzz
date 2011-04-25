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

