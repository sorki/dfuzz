from dfuzz.mut import zzuf

class FuzzWrapper(zzuf.FuzzWrapper):
    def __str__(self):
        return 'zzuf_10'

    def set_up(self, *args, **kwargs):
        super(FuzzWrapper, self).set_up(*args, **kwargs)

        self.seed_range = (0, 10)
