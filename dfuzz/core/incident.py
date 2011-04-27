import signal
import logging

class Incident(object):
    def __init__(self):
        self.crash_signals = '''
        SIGILL
        SIGABRT
        SIGBUS
        SIGFPE
        SIGSEGV
        '''

    @property
    def crash_signals(self):
        return self._crash_signals

    @crash_signals.setter
    def crash_signals(self, value):
        if type(value) == list:
            try:
                map(int, value)
            except ValueError:
                logging.error('crash_signals expects a list '
                    'of intergers or string of signal names. '
                    'No update - using old value.')
                return

            self._crash_signals = value

        elif type(value) == str:
            sep = ' '
            if ',' in value:
                sep = ','

            value = value.replace('\n', ' ')

            parts = map(lambda x: x.strip(), value.split(sep))
            new = []
            for i in parts:
                if len(i)==0:
                    continue
                if hasattr(signal, str(i)):
                    new.append(getattr(signal, str(i)))
                else:
                    logging.error('No such signal "%s" defined '
                        'in signal module', i)

            self._crash_signals = new

    def serious(self, retcode):
        return retcode in self.crash_signals
