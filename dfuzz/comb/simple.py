import logging

from dfuzz.core import utils
from dfuzz.core import wrapper

class FuzzWrapper(wrapper.DfuzzWrapper):
    def __str__(self):
        return 'combinator'

    def method(self):
        return 'comb'

    def set_up(self, input_file_path, tmp_dir_path, params):
        self.input = input_file_path
        self.output = tmp_dir_path
        self.params = params
        self.sane = False

        # defaults
        gen = 'dfuzz.gen.autodafe'
        mut = 'dfuzz.mut.zzuf_10'

        if len(self.params) > 0:
            if len(self.params) == 2:
                gen, mut = self.params
            else:
                logging.warning('Wrong %s parameter format,'
                    ' using defaults.', self)

        gen += '.FuzzWrapper'
        mut += '.FuzzWrapper'

        emsg = '[combinator] Unable to load class: "%s"'

        self.gen_cls = utils.get_class_by_path(gen)
        if not self.gen_cls:
            logging.error(emsg, gen)
            return

        self.mut_cls = utils.get_class_by_path(mut)
        if not self.mut_cls:
            logging.error(emsg, mut)
            return

        self.gen = self.gen_cls()
        self.mut = self.mut_cls()
        self.sane = True

    def run(self):
        if not self.sane:
            return

        self.gen.set_up(self.input, self.output, [])

        def generator():
            gen_generator = self.gen.run()
            for file in gen_generator():
                if file is None:
                    yield None # early error detection
                self.mut.set_up(file, self.output, [])
                mut_generator = self.mut.run()
                for mut_file in mut_generator():
                    yield mut_file

        return generator
