import re
import random
import logging

from dfuzz.core import utils

class ModuleLoader(object):
    def __init__(self):
        self.high_priority = []
        self.low_priority = []

    def shuffle(self):
        '''
        Randomize order of `self.high_priority and
        `self.low_priority` lists.
        '''

        random.shuffle(self.high_priority)
        random.shuffle(self.low_priority)

    def check_methods(self, cls, str_mod):
        '''
        Check whether `cls` class implements all
        the required methods.

        Module string `str_mod` used for logging purposes.
        '''

        required_methods = ['method', 'set_up', 'run']
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

        cls = utils.get_class_by_path(str_mod + '.FuzzWrapper')
        if not cls:
            logging.warning('Unable to load wrapper, skipping')
            return False
        else:
            if self.check_methods(cls, str_mod):
                return cls
            else:
                return False

    def add_valid_modules(self, str_mods, prior):
        '''
        Add valid modules from `str_mods` to `self.high_priority`
        and `self.low_priority` lists according to
        their priority - `prior`
        '''

        mod_strings = map(lambda x: x.strip(), str_mods.split(';'))

        # creates (cls, [params]) tuple

        for mod in mod_strings:
            if len(mod) == 0:
                continue

            params = []
            if '(' in mod:
                match = re.search('(.*)\((.*)\).*', mod)
                if match == None:
                    logging.warning('Bad format for module '
                        'parameters: %s. Skipping', mod)
                    continue

                mod = match.group(1).strip()
                params = match.group(2).strip()
                params = map(lambda x: x.strip(),
                    params.split(','))

            cls = self.validate_module(mod)
            if not cls:
                continue

            if prior == 'high':
                self.high_priority.append((cls, params))
            else:
                self.low_priority.append((cls, params))
