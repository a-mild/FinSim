from dataclasses import dataclass, field

import pandas as pd
from functools import lru_cache, reduce

import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta

from uuid import UUID, uuid4

from typing import List, Any, Dict

from src.components.traces.controls.datepicker import DatePicker
from src.components.traces.controls.interestpicker import InterestPicker
from src.components.traces.controls.valuepicker import ValuePicker
from src.components.traces.tracebase import Trace
from src.components.traces.tracewidget import TraceWidget


@dataclass
class ConstantPaymentTrace(Trace):
    side: str
    default_name: str = "Constant Payment"
    uuid: UUID = field(default_factory=uuid4)
    params: Dict = field(default_factory=lambda: {
        "from_date": (datetime.today() + pd.offsets.MonthBegin(-1)).normalize(),
        "to_date": (datetime.today() + pd.offsets.MonthBegin(-1)).normalize() + relativedelta(months=6),
        "value": 100.0,
        "interest": 0.0
    })

    def __post_init__(self):
        self.controls = [
            DatePicker("from_date", label="From Date", v_model=self.params["from_date"].strftime("%Y-%m")),
            DatePicker("to_date", label="To Date", v_model=self.params["to_date"].strftime("%Y-%m")),
            ValuePicker("value", v_model=str(self.params["value"])),
            InterestPicker("interest", v_model=str(self.params["interest"]))
        ]

    def get_timeseries(self, dti):
        array_length = len(dti)
        start_idx = dti.get_loc(self.params["from_date"])
        end_idx = dti.get_loc(self.params["to_date"])
        value = self.params["value"]
        q = 1 + self.params["interest"]/100
        interest_factor_per_month = pow(q, 1/12)
        return self.get_array(array_length, start_idx, end_idx, value, interest_factor_per_month)

    @staticmethod
    @lru_cache(maxsize=None)
    def get_array(array_length: int, start_idx: int, end_idx: int, value: float, q_m: float):
        delta = end_idx - start_idx
        triangles = [np.tri(delta, delta, -k) for k in range(1, delta+1)]
        interest_factors = np.power(q_m, reduce(np.add, triangles))
        value_triangle = np.tri(delta, delta, 0)*value
        result = np.sum(np.multiply(value_triangle, interest_factors), axis=1)
        parts = [np.zeros(start_idx),
                 result,
                 np.full(array_length-end_idx, result[-1])]
        return reduce(np.append, parts)

    def create_widget(self):
        return TraceWidget(
            side=self.side,
            uuid=self.uuid,
            name=self.default_name,
            controls=self.controls)


@dataclass
class SinglePaymentTrace(Trace):
    side: str
    default_name: str = "Single Payment"
    uuid: UUID = field(default_factory=uuid4)
    params: Dict = field(default_factory=lambda: {
        "date": datetime.today(),
        "value": 1000
    })


    def __post_init__(self):
        self.controls = [
            DatePicker("date", label="Date", v_model=self.params["date"].strftime("%Y-%m")),
            ValuePicker("value", v_model=str(self.params["value"]))
        ]


    # TODO: implement with get array
    def get_timeseries(self, dti):
        def compute_value(dt):
            if dt < self.params["date"]:
                return 0
            return self.params["value"]
        return [compute_value(dt) for dt in dti]

    def create_widget(self):
        return TraceWidget(
            side=self.side,
            uuid=self.uuid,
            name=self.default_name,
            controls=self.controls)
