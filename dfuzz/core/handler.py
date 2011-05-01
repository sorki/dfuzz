'''
Incident handler
'''

import os
import shutil
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

class FileIncidentHandler(CoreIncidentHandler):
    def handle_failure(self, target_obj, input_file_path):
        super(FileIncidentHandler, self).handle_failure(target_obj,
            input_file_path)

        out_dir_path = self.cfg.incidents_dir
        inc_dir_name = utils.parse_incident_fmt(self.cfg)
        work_dir = os.path.join(out_dir_path, inc_dir_name)
        os.mkdir(work_dir)

        shutil.copyfile(input_file_path, os.path.join(work_dir,
            self.cfg.incident_input))

        with open(os.path.join(work_dir,
            self.cfg.incident_stdout), 'w') as f:
            f.write(target_obj.stdout)

        with open(os.path.join(work_dir,
            self.cfg.incident_stderr), 'w') as f:
            f.write(target_obj.stderr)

        with open(os.path.join(work_dir,
            self.cfg.incident_info), 'w') as f:
            f.write(self.get_info_string(target_obj))

    def get_info_string(self, to):
        return (
            'Command line: "%s" \n\n'
            'Target return code: "%d" \n\n'
            'Fuzzing method: "%s"' %
            (to.cmd, to.code, self.fuzzer))

