

class Trace:
    tracetypes = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.tracetypes.update({cls.default_name: cls})

    @classmethod
    def tracenames(cls):
        return list(cls.tracetypes.keys())
