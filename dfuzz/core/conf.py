import os
import ConfigParser

import dfuzz

class Config(object):
    __dict = {}

    def __init__(self, path, filename='fuzz.conf'):
        config = ConfigParser.SafeConfigParser()
        def_cfg_path = os.path.join(
            os.path.dirname(dfuzz.__file__), 'cfg/defaults.ini')
        with open(def_cfg_path) as f:
            config.readfp(f)
        self._filepath = os.path.join(path, filename)
        config.read(self._filepath)

        setattr(self, 'work_dir', path)

        self._config = config
        for section in config.sections():
            for item in config.options(section):
                attr_name = item
                if section in ['generation', 'mutation', 'combination']:
                    attr_name = '%s_%s' % (section, item)

                value = config.get(section, item).strip()
                if value in ['0', '1']:
                    value = bool(int(value))

                setattr(self, attr_name, value)
                self.__dict[attr_name] = value
        return

    def as_dict(self):
        ''' This won't reflect any updates '''
        new_dict = {}
        for k, v in self.__dict.iteritems():
            new_dict[k] = getattr(self, k)

        self.__dict = new_dict
        return self.__dict
