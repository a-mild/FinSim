<v-list>
    <v-list-item>
        <v-list-item-title class="text-h6">
            {{name}}
            <v-menu v-model="menu" offset-y>
                <template v-slot:activator="{ on, attrs }">
                    <v-btn
                        icon
                        v-bind="attrs"
                        v-on="on"
                    >
                        <v-icon>mdi-plus-box</v-icon>
                    </v-btn>
                </template>
                <v-list>
                    <v-list-item v-for="name in tracenames" @click="add_trace(name)">
                        <v-list-item-title>{{name}}</v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-menu>
        </v-list-item-title>
    </v-list-item>
    <template v-for="w in tracewidgets" >
        <jupyter-widget :widget="w" />
    </template>

</v-list>