'''
Incident handler
'''

import logging

class IncidentHandler(object):
    def __init__(self, cfg, fuzzer):
        self.cfg = cfg
        self.fuzzer = fuzzer

    def handle_failure(self, target_obj, input_file_path):
        logging.debug('Handling failure')
        logging.debug('Command line: %s', target_obj.cmd)
        logging.debug('Target retcode: %d', target_obj.code)
        logging.debug('Target stdout: %s', target_obj.stdout)
        logging.debug('Target stderr: %s', target_obj.stderr)
        logging.debug('Fuzzing method: %s', self.fuzzer)
