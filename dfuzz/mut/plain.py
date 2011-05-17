import os
import shutil
import logging

from dfuzz.core import wrapper

class FuzzWrapper(wrapper.DfuzzWrapper):
    def __str__(self):
        return 'plain'

    def method(self):
        return 'mut'

    def set_up(self, input_file_path, tmp_dir_path, params):
        self.input = input_file_path
        self.output = tmp_dir_path
        self.params = params

    def run(self):
        out_path = os.path.join(self.output, 'plain.cfg')
        def generator():
            error = False
            try:
                shutil.copyfile(self.input, out_path)
            except IOError as e:
                logging.error('IO exception: %s', e)
                error = True

            if error:
                yield None
            else:
                yield out_path

        return generator
