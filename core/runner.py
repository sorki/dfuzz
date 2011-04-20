import logging

class ModuleRunner(object):
    def __init__(self, high_prio, low_prio):
        self.high_priority = high_prio
        self.low_priority  = low_prio

    def run(self):
        # spawn threads each running one module
        # TODO: thread priority
        for cls in self.high_priority:
            self.run_single(cls)
        # TODO: spawn low priority

    def run_single(self, cls):
        logging.debug('Instantiating class %s', cls)
        to_run = cls()
        logging.debug('[%s] Set up phase', to_run)
        to_run.set_up()
        logging.debug('[%s] Run phase', to_run)
        to_run.run()
        logging.debug('[%s] Tear down phase', to_run)
        to_run.tear_down()

