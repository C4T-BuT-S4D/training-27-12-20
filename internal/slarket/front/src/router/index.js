import Vue from 'vue';
import VueRouter from 'vue-router';

import Index from '@/views/Index';
import Me from '@/views/Me';
import User from '@/views/User';
import Login from '@/views/Login';
import Register from '@/views/Register';
import Catch from '@/views/Catch';
import SendMoney from '@/views/SendMoney';
import AccTrade from '@/views/AccTrade';

Vue.use(VueRouter);

const routes = [
    {
        path: '/',
        name: 'index',
        component: Index,
    },
    {
        path: '/me',
        name: 'me',
        component: Me,
    },
    {
        path: '/catch',
        name: 'catch',
        component: Catch,
    },
    {
        path: '/sendmoney',
        name: 'sendmoney',
        component: SendMoney,
    },
    {
        path: '/acctrade',
        name: 'acctrade',
        component: AccTrade,
    },
    {
        path: '/user/:username',
        name: 'user',
        component: User,
    },
    {
        path: '/login',
        name: 'login',
        component: Login,
    },
    {
        path: '/register',
        name: 'register',
        component: Register,
    },
];

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes,
});

export default router;
