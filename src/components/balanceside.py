import ipyvuetify as v
import ipywidgets as w
import traitlets

from blinker import signal

from src.components.traces import Trace
from src.enums import BalanceSides

add_trace = signal("add-trace")
delete_trace = signal("delete-trace")


class BalanceSide(v.VuetifyTemplate):
    template_file = "./src/components/balanceside.vue"

    name = traitlets.Unicode().tag(sync=True)
    menu = traitlets.Bool(False).tag(sync=True)
    tracewidgets = traitlets.Dict(default_value={}).tag(sync=True, **w.widget_serialization)

    tracenames = traitlets.List(default_value=Trace.tracenames()).tag(sync=True)
    
    def __init__(self, side: BalanceSides):
        self.side = side
        self.name = self.side.name
        super().__init__()
        delete_trace.connect(self.delete, sender=self.side)

    def vue_add_trace(self, tracename: str):
        new_trace: Trace = Trace.create_trace(self.side, tracename)
        #update the tracewidgets property
        new_widget = new_trace.create_widget()
        new_widgets = self.tracewidgets.copy()
        new_widgets.update({str(new_trace.uuid): new_widget})
        self.tracewidgets = new_widgets
        #send signal and let controller update the plot
        add_trace.send(self.side, trace=new_trace)

    def delete(self, sender, uuid):
        self.tracewidgets = {k: v for k, v in self.tracewidgets.items() if not k == str(uuid)}
