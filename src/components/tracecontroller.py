import ipyvuetify as v
import ipywidgets as w
import traitlets

from blinker import signal

from src.components.balanceside import BalanceSide


class TraceController(v.VuetifyTemplate):

    aktiva = traitlets.Any().tag(sync=True, **w.widget_serialization)
    passiva = traitlets.Any().tag(sync=True, **w.widget_serialization)

    drawer_open = traitlets.Bool(default_value=False).tag(sync=True)

    # TODO: put this in template file
    @traitlets.default('template')
    def _template(self):
        return """
        <template>
            <v-navigation-drawer app v-model="drawer_open">
                <jupyter-widget :widget="aktiva" />
                <v-divider></v-divider>
                <jupyter-widget :widget="passiva" />
            </v-navigation-drawer>    
        </template>
        """

    def __init__(self, model):
        self.model = model

        self.aktiva = BalanceSide("Aktiva")
        self.passiva = BalanceSide("Passiva")
        self.toggle_signal = signal("toggle-drawer")
        self.toggle_signal.connect(self.toggle_drawer)
        super().__init__()

    def toggle_drawer(self, sender):
        self.drawer_open = not self.drawer_open
