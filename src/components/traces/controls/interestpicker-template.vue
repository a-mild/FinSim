<template>
    <div>
        <v-checkbox
              v-model="use_interest"
              label="with fixed interest rate"
        >
        </v-checkbox>
        <v-text-field
            v-model="v_model"
            suffix="%"
            prepend-icon="mdi-percent"
            :disabled="!use_interest"
            :label="label"
            :rules="[
            () => !!v_model || 'Input required.',
            () => {
                const pattern = /^\d{1,3}(\.\d{0,5})?/;
                return pattern.test(v_model) || 'Invalid format (XXX.XXXXX)';}
            ]"
            @change="on_change()"
        >
        </v-text-field>
    </div>
</template>