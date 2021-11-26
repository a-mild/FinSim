<v-navigation-drawer app v-model="drawer_open" width="25%">
    <jupyter-widget :widget="sides.Aktiva" />
    <v-divider></v-divider>
    <jupyter-widget :widget="sides.Passiva" />
</v-navigation-drawer>
