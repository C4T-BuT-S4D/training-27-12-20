<template>
    <div class="master" v-if="user != null">
        <div class="info">
            <div>Имя: {{ user.имя }}</div>
            <div>Пароль: {{ user.пароль }}</div>
            <div>Баланс: {{ user.баланс }}</div>
        </div>

        <div class="slaves">
            <div class="slave" v-for="(slave, i) of user.слейвы" :key="i">
                <div>Имя: {{ slave.имя }}</div>
                <div>Владелец: {{ slave.владелец }}</div>
                <div>Описание: {{ slave.описание }}</div>
                <div>Цена: {{ slave.цена }}</div>
                <form @submit.prevent="send(slave.имя)">
                    <input type="text" v-model="form.кому" placeholder="кому" />
                    <input type="submit" value="Отправить" />
                </form>
            </div>
        </div>
    </div>
    <div v-else></div>
</template>

<script>
import { mapState } from 'vuex';

export default {
    computed: mapState(['user']),

    data: function() {
        return {
            form: {
                кому: '',
            },
        };
    },

    methods: {
        send: async function(кого) {
            try {
                await this.$http.post('/sleiv/torganut', {
                    ...this.form,
                    кого,
                });
                this.$router.push({ name: 'index' });
            } catch (e) {
                this.$toasted.error(e.response.data.err);
            }
        },
    },
};
</script>

<style lang="scss" scoped>
.master {
    .info {
        border: 1px solid black;
        padding: 1em;
    }

    .slaves {
        margin-top: 2em;

        display: flex;
        flex-flow: row wrap;

        .slave {
            border: 1px solid blue;
            flex: 0 0 auto;
            margin-right: 1em;
            margin-top: 0.5em;
            padding: 0.5em;
        }
    }
}
</style>
