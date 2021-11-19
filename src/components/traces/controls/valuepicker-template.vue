<template>
    <v-text-field
        v-model="v_model"
        prefix="$"
        prepend-icon="mdi-cash"
        :label="label"
        :rules="[
        () => !!v_model || 'Input required.',
        () => {
            const pattern = /^([1-9]{1}[0-9]{0,2}(\,\d{3})*(\.\d{0,2})?|[1-9]{1}\d{0,}(\.\d{0,2})?|0(\.\d{0,2})?|(\.\d{1,2}))$|^([1-9]{1}\d{0,2}(\,\d{3})*(\.\d{0,2})?|[1-9]{1}\d{0,}(\.\d{0,2})?|0(\.\d{0,2})?|(\.\d{1,2}))$|^\(\$?([1-9]{1}\d{0,2}(\,\d{3})*(\.\d{0,2})?|[1-9]{1}\d{0,}(\.\d{0,2})?|0(\.\d{0,2})?|(\.\d{1,2}))\)/;
            return pattern.test(v_model) || 'Invalid format (XXX,XXX.XX)';}
        ]"
        @change="on_change()"
    >
    </v-text-field>
</template>