import ipyvuetify as v
import traitlets

from src.components.traces import Trace


class BalanceSide(v.VuetifyTemplate):
    template_file = "./src/components/balanceside.vue"

    name = traitlets.Unicode("").tag(sync=True)
    menu = traitlets.Bool(False).tag(sync=True)
    widgets = traitlets.List().tag(sync=True)

    tracenames = traitlets.List(default_value=Trace.tracenames()).tag(sync=True)
    
    def __init__(self, name):
        self.name = name
        super().__init__()

    def vue_add_trace(self, tracename):
        print(tracename)

