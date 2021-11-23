from dataclasses import field
from marshmallow import Schema
import marshmallow_dataclass
from marshmallow_enum import EnumField

import pandas as pd
from functools import lru_cache, reduce

import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta

from uuid import UUID, uuid4

from typing import List, Any, Dict, ClassVar, Type

from src.components.traces.controls.datepicker import DatePicker
from src.components.traces.controls.interestpicker import InterestPicker
from src.components.traces.controls.valuepicker import ValuePicker
from src.components.traces.tracebase import Trace
from src.components.traces.tracewidget import TraceWidget
from src.enums import BalanceSides



@marshmallow_dataclass.dataclass
class SinglePaymentTrace(Trace):
    side: BalanceSides
    default_name: str = "Single Payment"
    uuid: UUID = field(default_factory=uuid4)
    params: Dict[str, Any] = field(default_factory=lambda: {
        "date": (datetime.today() + pd.offsets.MonthBegin(-1)).normalize(),
        "value": 1000,
        "interest": 0.0
    })
    Schema: ClassVar[Type[Schema]] = Schema

    def __post_init__(self):
        self.controls = [
            DatePicker("date", label="Date", v_model=self.params["date"].strftime("%Y-%m")),
            ValuePicker("value", v_model=str(self.params["value"])),
            InterestPicker("interest", v_model=str(self.params["interest"]))
        ]

    def get_timeseries(self, dti):
        array_length = len(dti)
        start_idx = dti.get_loc(self.params["date"])
        value = self.params["value"]
        q = 1 + self.params["interest"]/100
        interest_factor_per_month = pow(q, 1/12)
        result = self.get_array(array_length, start_idx, value, interest_factor_per_month)
        if self.side is BalanceSides.Passiva:
            result = -result
        return result

    @staticmethod
    @lru_cache(maxsize=None)
    def get_array(
            array_length: int,
            start_idx: int,
            value: float,
            q_m: float)\
            -> np.array:
        delta = array_length - start_idx
        array_values = np.ones(delta) * value
        array_interest = np.arange(delta)
        array_interest = np.power(q_m, array_interest)
        result = np.multiply(array_values, array_interest)
        return np.append(np.zeros(start_idx), result)

    def create_widget(self):
        return TraceWidget(
            side=self.side,
            uuid=self.uuid,
            name=self.default_name,
            controls=self.controls)


@marshmallow_dataclass.dataclass
class ConstantPaymentTrace(Trace):
    side: BalanceSides
    default_name: str = "Constant Payment"
    uuid: UUID = field(default_factory=uuid4)
    params: Dict[str, Any] = field(default_factory=lambda: {
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
        result = self.get_array(array_length, start_idx, end_idx, value, interest_factor_per_month)
        if self.side is BalanceSides.Passiva:
            result = -result
        return result

    @staticmethod
    @lru_cache(maxsize=None)
    def get_array(
            array_length: int,
            start_idx: int,
            end_idx: int,
            value: float,
            q_m: float)\
            -> np.array:
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
