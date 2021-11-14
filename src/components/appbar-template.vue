<template>
    <v-app-bar>
        <v-app-bar-nav-icon @click.stop="toggle_drawer()"></v-app-bar-nav-icon>
        <v-toolbar-title>
                Pension Simulator
                <div class="text-caption subheading">{{loaded_filename}}</div>
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon class="text-right" @click="reset_all()">
            <v-icon>mdi-refresh</v-icon>
        </v-btn>
        <jupyter-widget :widget="file_upload_widget" />
        <v-btn icon download class="text-right" @click="save_traces()">
            <v-icon>mdi-content-save</v-icon>
        </v-btn>
        <jupyter-widget :widget="file_download_dummy_outputwidget" />
    </v-app-bar>
</template>
