import os
import re
import shutil
import logging

from dfuzz.core import utils
from dfuzz.core import target
from dfuzz.core import incident

class ModuleRunner(object):
    def __init__(self, cfg, high_prio, low_prio):
        self.high_priority = high_prio
        self.low_priority  = low_prio
        self.cfg = cfg

    def run(self):
        '''
        Spawn threads according to configuration.
        '''

        # spawn threads each running one module
        # TODO: thread priority
        for cls in self.high_priority:
            self.run_single(cls)


        for cls in self.low_priority:
            self.run_single(cls)
        # TODO: spawn low priority

    def get_inputs(self, method):
        '''
        Get input files list from input directory
        corresponding to the used method (`method`_dir).

        Filter files according to `method`_dir_mask.
        '''

        out = []
        dir_path = getattr(self.cfg, "%s_dir" % method)
        dir_mask = getattr(self.cfg, "%s_dir_mask" % method)
        pattern = '^%s$' % dir_mask.replace('*', '.*')

        for root, dirs, files in os.walk(dir_path):
            for name in files:
                if re.match(pattern, name) == None:
                    logging.debug('File "%s" doesn\'t match '
                        'the mask "%s"', name, dir_mask)
                    continue

                out.append(os.path.join(root,name))

        return out

    def run_single(self, cls_tuple):
        '''
        Set up and run single instance of the class.
        This takes the input files, runs each of them through
        specific fuzzer (wrapper) and runs the executable
        with fuzzed input (via TargetRunner class).
        '''

        cls, params = cls_tuple
        logging.debug('Instantiating class %s', cls)
        to_run = cls()
        tmp_dir_path = os.path.join(self.cfg.tmp_dir, str(to_run))

        logging.debug('[%s] Creating tmp dir [%s]', to_run, tmp_dir_path)
        if os.path.isdir(tmp_dir_path):
            shutil.rmtree(tmp_dir_path)
        os.mkdir(tmp_dir_path)

        inputs = self.get_inputs(to_run.method())
        for input_file_path in inputs:
            logging.debug('[%s] Input file: "%s"', to_run,
                input_file_path)
            logging.debug('[%s] Set up phase', to_run)
            to_run.set_up(input_file_path, tmp_dir_path, params)
            logging.debug('[%s] Run phase', to_run)
            generator = to_run.run()
            if generator is None:
                logging.error('[%s] Terminating due to an error, '
                    ' no files supplied by the wrapper',
                    to_run)
                break

            for file in generator():
                if file is None:
                    logging.error('[%s] Skipping input file "%s" '
                        'due to an error', input_file_path, to_run)
                    break

                logging.debug('[%s] Using fuzzed file "%s"', to_run,
                    os.path.basename(file))

                if self.cfg.use_no_fuzz:
                    utils.handle_no_fuzz(file,
                        self.cfg.no_fuzz_file, self.cfg.use_no_fuzz)

                # TODO (minor): configurable classes
                targ = target.Target(self.cfg.binary, self.cfg.args)
                targ.run(file)

                inc = incident.Incident()
                inc.check(targ)


        if inputs == []:
            logging.warning('No input files for method "%s" found',
                to_run.method())

        logging.debug('[%s] Tear down phase', to_run)
        to_run.tear_down()
        logging.debug('[%s] Remove tmp dir', to_run)
        shutil.rmtree(tmp_dir_path)
