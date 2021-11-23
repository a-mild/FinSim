import ipyvuetify as v
import ipywidgets as w
import traitlets

import plotly.graph_objs as go

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
        self.tracecontroller_drawer = TraceController()
        self.app_bar = AppBar(model)
        self.plot_container = PlotContainer()
        trace = go.Scatter(x=self.model.df.index, y=self.model.df["sum"])
        self.plot_container.figure.add_trace(trace)
        super().__init__()
