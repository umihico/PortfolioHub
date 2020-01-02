
window.Vue = require('vue');

export * from './colors.js';

import '@mdi/font/css/materialdesignicons.css'
import Vuetify from 'vuetify';
import VueRouter from 'vue-router'
import cards_content from './components/CardsContent.vue';
import GithubButton from 'vue-github-button'

const routes = [
    {
        path: '/',
        name: 'root',
        component: cards_content
    },
];
const router = new VueRouter({
    mode: 'history',
    routes
});
import 'vuetify/dist/vuetify.min.css';
window.axios = require('axios');
Vue.use(Vuetify);
Vue.use(VueRouter);
export default new Vuetify({
    icons: {
        iconfont: 'mdi',
    },
})

const app = new Vue({
    router,
    vuetify: new Vuetify(),
    el: '#app',
    components:{
        cards_content,
        GithubButton,
    }
});
window.app=app;