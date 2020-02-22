/**
 * First we will load all of this project's JavaScript dependencies which
 * includes Vue and other libraries. It is a great starting point when
 * building robust, powerful web applications using Vue and Laravel.
 */

require('./bootstrap');

window.Vue = require('vue');

import '@mdi/font/css/materialdesignicons.css'
export * from './colors.js';
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css';
import VueRouter from 'vue-router'
import cards_content from './components/CardsContent.vue';
import GithubButton from 'vue-github-button'
Vue.use(Vuetify);
Vue.use(VueRouter);
/**
 * The following block of code may be used to automatically register your
 * Vue components. It will recursively scan this directory for the Vue
 * components and automatically register them with their "basename".
 *
 * Eg. ./components/ExampleComponent.vue -> <example-component></example-component>
 */

// const files = require.context('./', true, /\.vue$/i)
// files.keys().map(key => Vue.component(key.split('/').pop().split('.')[0], files(key).default))

Vue.component('example-component', require('./components/ExampleComponent.vue').default);

/**
 * Next, we will create a fresh Vue application instance and attach it to
 * the page. Then, you may begin adding components to this application
 * or customize the JavaScript scaffolding to fit your unique needs.
 */


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
window.axios = require('axios');
export default new Vuetify({
    icons: {
        iconfont: 'mdi',
    },
})
const app = new Vue({
    router,
    el: '#app',
    vuetify: new Vuetify(),
    components:{
        cards_content,
        GithubButton,
    }
});
window.app=app;