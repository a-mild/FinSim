import ipyvuetify as v
import ipywidgets as w
import traitlets

from blinker import signal

from src.components.balanceside import BalanceSide
from src.enums import BalanceSides


class TraceController(v.VuetifyTemplate):
    template_file = "./src/components/tracecontroller-template.vue"

    sides = traitlets.Dict(default_value={
        "Aktiva": BalanceSide(BalanceSides.Aktiva),
        "Passiva": BalanceSide(BalanceSides.Passiva)
    }).tag(sync=True, **w.widget_serialization)

    drawer_open = traitlets.Bool(default_value=False).tag(sync=True)

    def __init__(self):
        super().__init__()
        self.toggle_signal = signal("toggle-drawer")
        self.toggle_signal.connect(self.toggle_drawer)

    def toggle_drawer(self, sender):
        self.drawer_open = not self.drawer_open
