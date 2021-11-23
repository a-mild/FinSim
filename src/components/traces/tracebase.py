from src.components.traces.tracewidget import TraceWidget
from src.enums import BalanceSides


class Trace:
    # dictionary that holds all trace types that get registered as subclass of this class
    _tracetypes = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._tracetypes.update({cls.default_name: cls})

    @classmethod
    def tracenames(cls):
        return list(cls._tracetypes.keys())

    @classmethod
    def create_trace(cls, side: BalanceSides, tracename: str, **kwargs):
        class_ = cls._tracetypes[tracename]
        return class_(side)
