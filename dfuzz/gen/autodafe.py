import os
import logging

from dfuzz.core import wrapper
from dfuzz.core import exceptions

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
        try:
            self.system('adc %s %s' % (self.input,
                os.path.join(self.output, 'autodafe_compiled.adc')))

        except exceptions.SyscallException as e:
            logging.error('Autodafe compilation failed. Exception:'
                ' %s', e)
            return None

        adc_file = os.path.join(self.output, 'autodafe_compiled.adc')
        try:
            self.system('autodafe -v -f %s %s' % (self.output,
                adc_file))

        except exceptions.SyscallException as e:
            logging.error('Autodafe file generation failed. '
                'Exception: %s', e)
            return None

        os.remove(adc_file)

        def generator():
            for root, dirs, files in os.walk(self.output):
                for name in files:
                    if name == 'debugger.info':
                        continue
                    yield os.path.join(root, name)

        return generator

    def tear_down(self):
        pass
