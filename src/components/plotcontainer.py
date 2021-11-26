import ipyvuetify as v
import ipywidgets as w
import traitlets
import plotly.graph_objs as go

from src.model import Model


class PlotContainer(v.VuetifyTemplate):
    figure = traitlets.Any(
        go.FigureWidget(
            layout=dict(
                xaxis=dict(
                    rangeslider=dict(
                        visible=True
                    )
                ),
                margin=dict(l=20, r=20, t=20, b=20)
            )
        )).tag(sync=True, **w.widget_serialization)

    # TODO: put this in vue file
    template = traitlets.Unicode("""
        <v-main app class="mt-12">
            <jupyter-widget :widget="figure" />
        </v-main>
    """).tag(sync=True)

    def __init__(self, model: Model):
        self.model = model
        trace = go.Scatter(x=self.model.df.index, y=self.model.df["sum"])
        self.figure.add_trace(trace)
        super().__init__()
