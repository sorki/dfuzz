import os

from dfuzz.core import wrapper

class FuzzWrapper(wrapper.DfuzzWrapper):
    def __str__(self):
        return 'autodafe'

    def method(self):
        return 'gen'

    def set_up(self, input_file_path, tmp_dir_path, params):
        self.input = input_file_path
        self.output = tmp_dir_path
        self.autodafe_params = params

    def run(self):
        out_path = os.path.join(self.output, 'zzuf.cfg')
        self.system()
        def generator():
            for seed in range(*self.seed_range):
                self.system('zzuf -s%d -r%s < %s > %s' % (seed,
                    '%s:%s' % self.ratio, self.input, out_path))
                yield out_path

        return generator

    def tear_down(self):
        pass
