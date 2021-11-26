<template>
    <v-app-bar app>
        <v-app-bar-nav-icon @click.stop="toggle_drawer()"></v-app-bar-nav-icon>
        <v-toolbar-title class=".text-h5">
                Pension Simulator
                <div style="font-size: 0.6em">{{loaded_filename}}</div>
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-dialog
            v-model="reset_traces_dialog"
            width="500"
        >
            <template v-slot:activator="{ on, attrs }">
                <v-btn
                    icon
                    v-bind="attrs"
                    v-on="on"
                >
                    <v-icon>mdi-trash-can</v-icon>
                </v-btn>
            </template>
            <v-card>
                <v-card-title class="text-h5 grey lighten-2">
                    Warning
                </v-card-title>
                <v-card-text>
                    Are you sure you want to reset all traces?
                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions>
                    <v-btn
                        color="green"
                        text
                        @click="reset_traces()"
                    >
                        Yes!
                    </v-btn>
                    <v-btn
                        color="red"
                        text
                        @click="reset_traces_dialog = false"
                    >
                        No!
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <jupyter-widget :widget="file_upload_widget" />
        <v-btn icon download class="text-right" @click="save_traces()">
            <v-icon>mdi-content-save</v-icon>
        </v-btn>
        <jupyter-widget :widget="file_download_dummy_outputwidget" />
    </v-app-bar>
</template>
