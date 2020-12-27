import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        user: null,
        userRequested: false,
    },

    mutations: {
        SET_USER: (state, user) => {
            state.user = user;
        },
    },

    actions: {
        UPDATE_USER: async function(context) {
            try {
                const r = await this.$http.get('/polzovateli/ya');
                context.commit('SET_USER', r.data.ok);
            } catch (e) {
                context.commit('SET_USER', null);
            }
        },
    },
    modules: {},
});
