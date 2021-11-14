import copy

import ipyvuetify as v
import ipywidgets as w
import traitlets
from traitlets import observe

from src.components.tracecontroller import TraceController
from src.components.appbar import AppBar
from src.components.plotcontainer import PlotContainer

class App(v.VuetifyTemplate):
    tracecontroller_drawer = traitlets.Any().tag(sync=True, **w.widget_serialization)
    app_bar = traitlets.Any().tag(sync=True, **w.widget_serialization)
    plot_container = traitlets.Any().tag(sync=True, **w.widget_serialization)
    drawer_open = traitlets.Bool(default_value=False).tag(sync=True)

    template = traitlets.Unicode("""
        <template>
            <v-app>
                <jupyter-widget :widget="tracecontroller_drawer" />
                <jupyter-widget :widget="app_bar" />
                <jupyter-widget :widget="plot_container" />
            </v-app>
        </template>
    """).tag(sync=True)


    def __init__(self, model):
        self.model = model
        super().__init__()
        self.tracecontroller_drawer = TraceController(model)
        self.app_bar = AppBar(model)
        self.plot_container = PlotContainer(parent=self)


    def toggle_drawer(self, data=None):
        print("toggle drawer in parent")
        x = copy.deepcopy(self.tracecontroller_drawer.drawer_open)
        self.tracecontroller_drawer.drawer_open = not x

    def toggled(self, change):
        print(type(change["old"]))
        print(change["old"])
        print(type(change["new"]))
        print(change["new"])
        print(self.drawer_open)

