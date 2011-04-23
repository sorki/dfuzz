import os
import logging

from dfuzz.core import wrapper

class FuzzWrapper(wrapper.DfuzzWrapper):
    def __str__(self):
        return 'zzuf'

    def method(self):
        return 'mut'

    def set_up(self, input_file_path, tmp_dir_path, params):
        self.input = input_file_path
        self.output = tmp_dir_path
        self.zzuf_params = params

        # TODO (major): parse zzuf_params
        self.ratio = (.004, .01)
        self.seed_range = (2, 7)

    def run(self):
        try:
            self.system('zzzuf -V')
        except wrapper.SyscallException as e:
            logging.error('Unable to call "zzuf -V", is zzuf'
                ' installed? Exception: %s', e)
            return None

        out_path = os.path.join(self.output, 'zzuf.cfg')
        def generator():
            for seed in range(*self.seed_range):
                self.system('zzuf -s%d -r%s < %s > %s' % (seed,
                    '%s:%s' % self.ratio, self.input, out_path))
                yield out_path

        return generator

    def tear_down(self):
        pass
