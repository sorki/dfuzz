import os
import logging

from dfuzz.core import wrapper
from dfuzz.core import exceptions

class FuzzWrapper(wrapper.DfuzzWrapper):
    def __str__(self):
        return 'zzuf'

    def method(self):
        return 'mut'

    def set_up(self, input_file_path, tmp_dir_path, params):
        self.input = input_file_path
        self.output = tmp_dir_path
        self.zzuf_params = params

        # defaults
        ratio_start = .001
        ratio_end = .004
        seed_max = 10000

        if len(self.zzuf_params) > 0:
            try:
                if len(self.zzuf_params) == 2:
                    ratio_start = float(self.zzuf_params[0])
                    ratio_end = ratio_start + 0.001
                    seed_max = self.zzuf_params[1]
                elif len(self.zzuf_params) == 3:
                    ratio_start = float(self.zzuf_params[0])
                    ratio_end = float(self.zzuf_params[1])
                    seed_max = self.zzuf_params[2]
                else:
                    logging.warning('Wrong %s parameter format,'
                        ' using defaults.', self)
            except ValueError as e:
                logging.warning('Unable to parse attributes'
                    ' passed to %s. Using default values. '
                    ' Check your config. Exception: %s', self, e)

        self.ratio = (ratio_start, ratio_end)
        self.seed_range = (0, int(seed_max))

    def run(self):
        try:
            self.system('zzuf -V')
        except exceptions.SyscallException as e:
            logging.error('Unable to call "zzuf -V", is zzuf'
                ' installed? Exception: %s', e)
            return None

        out_path = os.path.join(self.output, 'zzuf.cfg')
        def generator():
            error = False
            for seed in range(*self.seed_range):

                try:
                    self.system('zzuf -s%d -r%s < %s > %s' % (seed,
                        '%s:%s' % self.ratio, self.input, out_path))
                except exceptions.SyscallException as e:
                    logging.error('System call exception: %s', e)
                    error = True
                    break

                yield out_path

            if error:
                yield None

        return generator

    def tear_down(self):
        pass
