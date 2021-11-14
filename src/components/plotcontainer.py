import ipyvuetify as v
import traitlets


class PlotContainer(v.VuetifyTemplate):
    template = traitlets.Unicode("""
        <template>
            <v-main>
            Hello world!
            </v-main
        </template>        
    """).tag(sync=True)
