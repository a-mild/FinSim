from dataclasses import dataclass

from src.components.traces.tracebase import Trace


@dataclass
class ConstantPaymentTrace(Trace):
    default_name: str = "Constant Payment"


@dataclass
class SinglePaymentTrace(Trace):
    default_name: str = "Single Payment"
