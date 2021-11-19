from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import datetime

from uuid import UUID

import pandas as pd
from typing import Dict, Any, List

from src.components.traces import Trace


@dataclass
class Model:
    start_date: datetime = datetime.today()
    periods: int = 120
    traces: OrderedDict = field(default_factory=OrderedDict)

    def __post_init__(self):
        # prepare the dataframe, freq month start so the timeseries functions work
        # make sure to include current month
        self.start_date = (self.start_date + pd.offsets.MonthBegin(-1)).normalize()
        dti = pd.date_range(self.start_date, periods=self.periods, freq="MS", normalize=True)
        self.df = pd.DataFrame(index=dti, columns=["sum"])
        self.df.loc[:, "sum"] = 0

    def get_xlims(self):
        idx = self.df.index
        return (idx[0].date(), idx[-1].date())

    def add_trace(self, trace: Trace):
        self.traces.update({trace.uuid: trace})
        ts = trace.get_timeseries(self.df.index)
        self.df[trace.uuid] = ts
        self.update_sum_column()

    def delete_trace(self, uuid: UUID):
        self.traces.pop(uuid)
        self.df.drop(uuid, inplace=True)
        self.update_sum_column()

    def update_trace(self, uuid: UUID, params: Dict[str, Any]):
        trace = self.traces[uuid]
        trace.params.update(params)
        ts = trace.get_timeseries(self.df.index)
        self.df[uuid] = ts
        self.update_sum_column()

    def update_sum_column(self):
        """Exclude sum column and compute sum of each month"""
        self.df["sum"] = self.df[self.df.columns.difference(["sum"])].sum(axis=1)

    def get_sum_column(self) -> List[int]:
        return self.df["sum"].tolist()

    def get_trace_idx(self, uuid: UUID) -> int:
        return self.traces.keys().index(uuid)

    #TODO
    def reset_all(self):
        """Reset all traces"""
        return

    #TODO
    def to_json(self) -> str:
        """Return a json string of the current state of the traces"""
        return

    #TODO
    def from_json(self, json_str: str):
        """Load a state from a json string document"""
        return