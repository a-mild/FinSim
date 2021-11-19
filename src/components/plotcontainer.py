import ipyvuetify as v
import ipywidgets as w
import traitlets
import plotly.graph_objs as go


class PlotContainer(v.VuetifyTemplate):
    figure = traitlets.Any(go.FigureWidget()).tag(sync=True, **w.widget_serialization)

    # TODO: put this in vue file
    template = traitlets.Unicode("""
        <template>
            <v-main app>
                <jupyter-widget :widget="figure" />
            </v-main>
        </template>        
    """).tag(sync=True)

    def __init__(self):
        super().__init__()