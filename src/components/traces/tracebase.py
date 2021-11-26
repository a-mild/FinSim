from dataclasses import field

from uuid import UUID, uuid4

from typing import Any, Dict, ClassVar

import marshmallow_dataclass

from src.components.traces.tracewidget import TraceWidget
from src.enums import BalanceSides


@marshmallow_dataclass.dataclass
class Trace:
    side: BalanceSides
    params: Dict[str, Any]
    default_name: str
    uuid: UUID = field(default_factory=uuid4)

    # dictionary that holds all trace types that get registered as subclass of this class
    _tracetypes: ClassVar[Dict[str, Any]] = {}

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
