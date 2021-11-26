from dataclasses import field
from marshmallow import Schema
import marshmallow_dataclass
from marshmallow_enum import EnumField

import pandas as pd
from functools import lru_cache, reduce

import numpy as np
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from uuid import UUID, uuid4

from typing import List, Any, Dict, ClassVar, Type, Union

from src.utils import utils
from src.components.traces.controls.datepicker import DatePicker
from src.components.traces.controls.interestpicker import InterestPicker
from src.components.traces.controls.valuepicker import ValuePicker
from src.components.traces.tracebase import Trace
from src.components.traces.tracewidget import TraceWidget
from src.enums import BalanceSides



@marshmallow_dataclass.dataclass
class SinglePaymentParameters:
    date: datetime = field(default_factory=utils.get_BOM_datetime)
    value: float = 1000.0
    interest: float = 0.0


@marshmallow_dataclass.dataclass
class SinglePaymentTrace(Trace):
    side: BalanceSides
    default_name: str = "Single Payment"
    params: SinglePaymentParameters = field(default_factory=lambda: SinglePaymentParameters())

    Schema: ClassVar[Type[Schema]] = Schema

    def __post_init__(self):
        self.controls = [
            DatePicker("date", label="Date", v_model=self.params.date.strftime("%Y-%m")),
            ValuePicker("value", v_model=str(self.params.value)),
            InterestPicker("interest", v_model=str(self.params.interest))
        ]

    def get_timeseries(self, dti):
        array_length = len(dti)
        start_idx = dti.get_loc(self.params.date)
        value = self.params.value
        q = 1 + self.params.interest/100
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
class ConstantPaymentParameters:
    from_date: datetime = field(default_factory=utils.get_BOM_datetime)
    to_date: datetime = field(
        default_factory=lambda: utils.get_BOM_datetime(
            datetime.today() + relativedelta(months=6)
        )
    )
    value: float = 100.0
    interest: float = 0.0


@marshmallow_dataclass.dataclass
class ConstantPaymentTrace(Trace):
    side: BalanceSides
    default_name: str = "Constant Payment"
    params: ConstantPaymentParameters = field(default_factory=lambda: ConstantPaymentParameters())

    Schema: ClassVar[Type[Schema]] = Schema

    def __post_init__(self):
        self.controls = [
            DatePicker("from_date", label="From Date", v_model=self.params.from_date.strftime("%Y-%m")),
            DatePicker("to_date", label="To Date", v_model=self.params.to_date.strftime("%Y-%m")),
            ValuePicker("value", v_model=str(self.params.value)),
            InterestPicker("interest", v_model=str(self.params.interest))
        ]

    def get_timeseries(self, dti):
        array_length = len(dti)
        start_idx = dti.get_loc(self.params.from_date)
        end_idx = dti.get_loc(self.params.to_date)
        value = self.params.value
        q = 1 + self.params.interest/100
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
