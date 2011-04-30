'''
Incident handler
'''

import logging

class ConsoleIncidentHandler(object):
    def __init__(self, cfg, fuzzer):
        self.cfg = cfg
        self.fuzzer = fuzzer

    def handle_failure(self, target_obj, input_file_path):
        def log_fn(str):
            logging.warning('[%s] %s' % (self.fuzzer, str))

        log_fn('Handling failure')
        log_fn('Command line: %s'% target_obj.cmd)
        log_fn('Target retcode: %d'% target_obj.code)
        log_fn('Target stdout: %s'% target_obj.stdout)
        log_fn('Target stderr: %s'% target_obj.stderr)
        log_fn('Fuzzing method: %s'% self.fuzzer)
