'''
Incident handler
'''

import os
import logging

from dfuzz.core import utils


class CoreIncidentHandler(object):
    def __init__(self, cfg, fuzzer):
        self.cfg = cfg
        self.fuzzer = fuzzer
        self.cfg.handler_semaphore.acquire()

    def __del__(self):
        self.cfg.handler_semaphore.release()

    def handle_failure(self, target_obj, input_file_path):
        self.cfg.num_incidents += 1
        logging.warning('[%s] Handling incident', self.fuzzer)

class ConsoleIncidentHandler(CoreIncidentHandler):
    def handle_failure(self, target_obj, input_file_path):
        super(ConsoleIncidentHandler, self).handle_failure(target_obj,
            input_file_path)

        def log_fn(str):
            logging.warning('[%s] %s' % (self.fuzzer, str))

        log_fn('Command line: %s'   % target_obj.cmd)
        log_fn('Target retcode: %d' % target_obj.code)
        log_fn('Target stdout: %s'  % target_obj.stdout)
        log_fn('Target stderr: %s'  % target_obj.stderr)
        log_fn('Fuzzing method: %s' % self.fuzzer)

class FileIncidentHandler(object):
    def handle_failure(self, target_obj, input_file_path):
        super(ConsoleIncidentHandler, self).handle_failure(target_obj,
            input_file_path)

        #os.mkdir(utils.parse_incident_fmt(self.cfg))
