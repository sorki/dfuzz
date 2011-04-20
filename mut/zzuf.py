class FuzzWrapper(object):
    def __str__(self):
        return 'zzuf'

    def method(self):
        return 'mut'

    def set_up(self, input_file_path, tmp_dir_path, params):
        self.input = input_file_path
        self.output = tmp_dir_path
        self.zzuf_params = params

    def run(self):
        def generator():
            # exec zzuf
            # return outputfname
            for name in range(10):
                yield self.output + str(name)

        return generator

    def tear_down(self):
        pass
