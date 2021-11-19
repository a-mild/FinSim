<v-menu
    v-model="menu"
    :close-on-content-click="false"
    transition="scale-transition"
    offset-y
    min-width="290px"
    dark
>
    <template v-slot:activator="{ on, attrs }">
        <v-text-field
        v-model="v_model"
        :label="label"
        prepend-icon="mdi-calendar"
        readonly
        v-bind="attrs"
        v-on="on"          >
    </v-text-field>
    </template>
    <v-date-picker
        v-model="v_model"
        type="month"
        reactive
        dark
        @input="menu = false"
    >
    </v-date-picker>
</v-menu>