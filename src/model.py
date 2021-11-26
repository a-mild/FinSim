import marshmallow_dataclass
from marshmallow import Schema
from dataclasses import field
from datetime import datetime

from uuid import UUID

import pandas as pd
from typing import Dict, Any, List, Union, ClassVar, Type

from src.utils import utils
from src.components.traces import Trace
from src.components.traces.traces import SinglePaymentTrace, ConstantPaymentTrace


@marshmallow_dataclass.dataclass
class Model:
    # make sure start_date is beginning of month
    start_date: datetime = field(
        default_factory=utils.get_BOM_datetime
    )
    periods: int = 480
    traces: Dict[UUID, Union[SinglePaymentTrace, ConstantPaymentTrace]] = field(default_factory=dict)

    Schema: ClassVar[Type[Schema]] = Schema

    def __post_init__(self):
        self.init_dataframe()

    def init_dataframe(self) -> None:
        dti = pd.date_range(self.start_date, periods=self.periods, freq="MS", normalize=True)
        self.df = pd.DataFrame(index=dti, columns=["sum"])
        self.df.loc[:, "sum"] = 0
        # if model gets loaded with existing traces, recalculate the df
        for uuid, trace in self.traces.items():
            ts = trace.get_timeseries(self.df.index)
            self.df[str(uuid)] = ts
        self.update_sum_column()

    def add_trace(self, trace: Trace):
        self.traces.update({trace.uuid: trace})
        ts = trace.get_timeseries(self.df.index)
        self.df[str(trace.uuid)] = ts
        self.update_sum_column()

    def delete_trace(self, uuid: UUID):
        self.traces.pop(uuid)
        self.df.drop(columns=str(uuid), inplace=True)
        self.update_sum_column()

    def reset_traces(self):
        self.traces.clear()
        self.init_dataframe()

    def update_trace(self, uuid: UUID, paramname: str, value) -> None:
        trace = self.traces[uuid]
        setattr(trace.params, paramname, value)
        ts = trace.get_timeseries(self.df.index)
        self.df[str(uuid)] = ts
        self.update_sum_column()

    def update_sum_column(self):
        """Exclude sum column and compute sum of each month"""
        self.df["sum"] = self.df[self.df.columns.difference(["sum"])].sum(axis=1)

    def get_sum_column(self) -> List[float]:
        return self.df["sum"].tolist()

    def get_trace_idx(self, uuid: UUID) -> int:
        return self.traces.keys().index(uuid)

    def to_json(self) -> str:
        """Return a json string of the current state of the traces"""
        return self.Schema().dumps(self)

    #TODO
    def from_json(self, json_str: str):
        """Load a state from a json string document"""
        return