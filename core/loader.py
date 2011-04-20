import random
import logging

class ModuleLoader(object):
    def __init__(self):
        self.high_priority = []
        self.low_priority = []

    def shuffle(self):
        random.shuffle(self.high_priority)
        random.shuffle(self.low_priority)

    def check_methods(self, cls, str_mod):
        '''
        Check whether `cls` class implements all
        the required methods.

        Module string `str_mod` used for logging purposes.
        '''

        required_methods = ['set_up', 'run', 'tear_down']
        for method in required_methods:
            if not hasattr(cls, method):
                logging.warning('"FuzzWrapper" class in module "%s"'
                    ' has no method "%s", skipping' %
                    (str_mod, method))
                return False

        return True

    def validate_module(self, str_mod):
        '''
        Try to import and load `str_mod` module,
        check required methods.

        Returns class for valid classes, False otherwise.
        '''

        try:
            mod = __import__(str_mod, fromlist=['a'])
        except ImportError:
            logging.warning('No such module: "%s", skipping' % str_mod)
            return False

        if hasattr(mod, 'FuzzWrapper'):
            cls = getattr(mod, 'FuzzWrapper')
            if self.check_methods(cls, str_mod):
                return cls
            else:
                return False

        logging.warning('Module "%s" has no "FuzzWrapper" class,'
            ' skipping' % str_mod)
        return False

    def add_valid_modules(self, str_mods, prior):
        '''
        Add valid modules from `str_mods` to `self.high_priority`
        and `self.low_priority` lists according to
        their priority - `prior`
        '''

        mod_strings = map(lambda x: x.strip(), str_mods.split(','))
        for mod in mod_strings:
            cls = self.validate_module(mod)
            if not cls:
                continue

            if prior == 'high':
                self.high_priority.append(cls)
            else:
                self.low_priority.append(cls)

