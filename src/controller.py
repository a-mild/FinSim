from typing import Any, Dict

from uuid import UUID

from blinker import signal

from src.app import App
from src.components.traces import Trace
from src.model import Model

add_trace = signal("add-trace")
delete_trace = signal("delete-trace")
update_trace = signal("update-trace")


class Controller:

    def __init__(self, model: Model, app: App):
        self.model = model
        self.app = app
        add_trace.connect(self.add_trace)
        delete_trace.connect(self.delete_trace)
        update_trace.connect(self.update_trace)

    def add_trace(self, sender, trace: Trace) -> None:
        self.model.add_trace(trace)
        sum_col = self.model.get_sum_column()
        self.app.plot_container.figure.data[0].y = sum_col

    def delete_trace(self, sender, uuid: UUID) -> None:
        idx = self.model.get_trace_idx(uuid)
        self.model.delete_trace(uuid)
        sum_col = self.model.get_sum_column()
        self.app.plot_container.figure.data[0].y = sum_col

    def update_trace(self, sender, params: Dict[str, Any]) -> None:
        self.model.update_trace(sender, params)
        sum_col = self.model.get_sum_column()
        self.app.plot_container.figure.data[0].y = sum_col
