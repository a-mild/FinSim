from typing import Any, Dict

from uuid import UUID

from blinker import signal

from src.app import App
from src.components.traces import Trace
from src.enums import BalanceSides
from src.model import Model

add_trace = signal("add-trace")
delete_trace = signal("delete-trace")
update_trace = signal("update-trace")
save_traces = signal("save-traces")
upload_traces = signal("upload-traces")
reset_traces = signal("reset-traces")


class Controller:

    def __init__(self, model: Model, app: App):
        self.model = model
        self.app = app
        add_trace.connect(self.add_trace)
        delete_trace.connect(self.delete_trace)
        update_trace.connect(self.update_trace)
        reset_traces.connect(self.reset_traces)
        save_traces.connect(self.save_traces)
        upload_traces.connect(self.upload_traces)


    def add_trace(self, sender: BalanceSides, tracename: str) -> None:
        new_trace: Trace = Trace.create_trace(sender, tracename)
        self.model.add_trace(new_trace)
        self.add_tracewidget(new_trace)
        self.update_plot()

    def delete_trace(self, sender: BalanceSides, uuid: UUID) -> None:
        # update the tracecontroller view
        self.app.tracecontroller_drawer.sides[sender.name].delete_trace(uuid)
        # update the model
        self.model.delete_trace(uuid)
        self.update_plot()

    def add_tracewidget(self, trace: Trace) -> None:
        # create tracewidget and add it to the tracecontroller view
        side = trace.side.name
        new_widget = trace.create_widget()
        self.app.tracecontroller_drawer.sides[side].add_tracewidget(new_widget)

    def update_plot(self) -> None:
        sum_col = self.model.get_sum_column()
        self.app.plot_container.figure.data[0].y = sum_col

    def update_trace(self, sender: UUID, paramname: str, value) -> None:
        self.model.update_trace(sender, paramname, value)
        self.update_plot()

    def reset_traces(self, sender=None) -> None:
        self.model.reset_traces()
        self.app.tracecontroller_drawer.sides[BalanceSides.Aktiva.name].tracewidgets = []
        self.app.tracecontroller_drawer.sides[BalanceSides.Passiva.name].tracewidgets = []
        self.update_plot()

    def save_traces(self, sender=None) -> None:
        payload = self.model.to_json()
        self.app.app_bar.trigger_file_download(
            payload,
            'pensionsimulator.json',
            kind='text/json'
        )

    def upload_traces(self, sender, filename: str, content: str) -> str:
        # TODO: maybe refactor this into a context manager
        try:
            loaded = Model.Schema().loads(content)
        except Exception as e:
            return f"Error loading file {filename!r}"
        else:
            self.model = loaded
            self.app.tracecontroller_drawer.sides[BalanceSides.Aktiva.name].tracewidgets = []
            self.app.tracecontroller_drawer.sides[BalanceSides.Passiva.name].tracewidgets = []
            for trace in self.model.traces.values():
                self.add_tracewidget(trace)
            self.update_plot()
            return f"Loaded file: {filename!r}"
