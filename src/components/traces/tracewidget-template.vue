<v-list-group sub-group no-action class="pl-0">
    <template v-slot:activator>
        <v-list-item-content>
            <v-list-item-title>{{ name }}</v-list-item-title>
        </v-list-item-content>
        <v-spacer></v-spacer>
        <v-list-item-icon @click="change_tracename()">
            <v-icon disabled>mdi-pencil</v-icon>
        </v-list-item-icon>
        <v-list-item-icon @click="delete_trace()">
            <v-icon>mdi-trash-can</v-icon>
        </v-list-item-icon>
    </template>
    <template v-for="c in controls">
        <jupyter-widget :widget="c" />
    </template>
</v-list-group>