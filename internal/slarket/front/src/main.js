import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import axios from 'axios';
import Toasted from 'vue-toasted';

let url = '';

if (process.env.NODE_ENV === 'development') {
    url = 'http://localhost:3001';
} else {
    url = window.location.origin;
}

const apiUrl = `${url}/rychka`;

axios.defaults.baseURL = apiUrl;
axios.defaults.withCredentials = true;

Vue.prototype.$http = axios;
store.$http = axios;

Vue.use(Toasted, {
    position: 'bottom-right',
    duration: 2000,
});

Vue.config.productionTip = false;

new Vue({
    router,
    store,
    render: h => h(App),
}).$mount('#app');
