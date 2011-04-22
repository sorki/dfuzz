import os

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

    def run(self):
        out_path = os.path.join(self.output, 'zzuf.cfg')
        def generator():
            for name in range(10):
                self.system('zzuf < %s > %s' % (self.input, out_path))
                yield out_path

        return generator

    def tear_down(self):
        pass
