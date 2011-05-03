import signal
import logging

class Incident(object):
    def __init__(self, cfg, fuzzer, handler_cls):
        self.crash_signals = '''
        SIGILL
        SIGABRT
        SIGBUS
        SIGFPE
        SIGSEGV
        '''

        self.cfg = cfg
        self.handler_cls = handler_cls
        self.fuzzer = fuzzer

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
        return -retcode in self.crash_signals

    def check(self, target_obj, input_file_path):
        logging.debug(target_obj.code)
        if self.serious(target_obj.code):
            handler = self.handler_cls(self.cfg, self.fuzzer)
            handler.handle_failure(target_obj, input_file_path)

class TimeIncident(Incident):
    def __init__(self, *args, **kwargs):
        super(TimeIncident, self).__init__(*args, **kwargs)
        self.crash_signals.append(signal.SIGKILL)
