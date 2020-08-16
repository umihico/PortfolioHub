<template>
    <transition name="fade">
        <v-pagination
            v-model="data_page"
            @input="paginate()"
            :length="last_page"
            :total-visible="8"
            v-if="show_pagination"
        ></v-pagination>
    </transition>
</template>
<script>
    import {
        VPagination,
    } from "vuetify/lib";

    export default {
        name: "pagination",
        props: ['page'],
        components: {
            VPagination,
        },
        data() {
            return {
                data_page: this.page,
                last_page: null,
                show_pagination: false,
            };
        },
        methods: {
            show(last_page) {
                this.show_pagination = true;
                this.last_page = last_page;
            },
            paginate() {
                this.$emit('pageHandler', this.data_page);
            },
        },
    };
</script>
