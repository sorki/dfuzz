class Config(object):
    pass

class TargetObj(object):
    pass

class Handler(object):
    def __init__(self, cfg, fuzzer):
        self.cfg = cfg
        self.fuzzer = fuzzer

    def handle_failure(self, target_obj, input_file_path):
        self.target_obj = target_obj
        self.input_file_path = input_file_path
