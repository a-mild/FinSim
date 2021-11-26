from uuid import UUID

import ipyvuetify as v
import ipywidgets as w
import traitlets

from blinker import signal

from src.components.traces import Trace
from src.components.traces.tracewidget import TraceWidget
from src.enums import BalanceSides

add_trace = signal("add-trace")
delete_trace = signal("delete-trace")


class BalanceSide(v.VuetifyTemplate):
    template_file = "./src/components/balanceside-template.vue"

    name = traitlets.Unicode().tag(sync=True)
    menu = traitlets.Bool(False).tag(sync=True)
    tracewidgets = traitlets.List(default_value=[]).tag(sync=True, **w.widget_serialization)

    tracenames = traitlets.List(default_value=Trace.tracenames()).tag(sync=True)
    
    def __init__(self, side: BalanceSides):
        self.side = side
        self.name = self.side.name
        super().__init__()

    def vue_add_trace(self, tracename: str) -> None:
        #send signal and let controller add trace to the model and update the plot
        add_trace.send(self.side, tracename=tracename)

    def add_tracewidget(self, new_widget: TraceWidget) -> None:
        self.tracewidgets = self.tracewidgets + [new_widget]

    def delete_trace(self, uuid: UUID) -> None:
        self.tracewidgets = [w for w in self.tracewidgets if not w.uuid == uuid]
