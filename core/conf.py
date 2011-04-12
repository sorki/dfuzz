import os
import ConfigParser


class Config(object):
    def __init__(self, path, filename='fuzz.conf'):
        config = ConfigParser.RawConfigParser()
        self._filepath = os.path.abspath(os.path.join(
            os.path.expanduser(path), filename))
        config.read(self._filepath)

        self._config = config
        for section in config.sections():
            for item in config.options(section):
                attr_name = item
                if section in ['generation', 'mutation', 'combination']:
                    attr_name = '%s_%s' % (section, item)
                setattr(self, attr_name, config.get(section, item).strip())
        return

settings = Config()
