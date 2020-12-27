<template>
    <div class="master" v-if="user != null">
        <div class="info">
            <div>Имя: {{ user.имя }}</div>
            <div>Баланс: {{ user.баланс }}</div>
        </div>

        <div class="slaves">
            <div class="slave" v-for="(slave, i) of user.слейвы" :key="i">
                <div>Имя: {{ slave.имя }}</div>
                <div>Владелец: {{ slave.владелец }}</div>
                <div>Описание: {{ slave.описание }}</div>
                <div>Цена: {{ slave.цена }}</div>
            </div>
        </div>
    </div>
    <div v-else></div>
</template>

<script>
export default {
    data: function() {
        return {
            user: null,
        };
    },

    created: async function() {
        const { username } = this.$route.params;

        try {
            const {
                data: { ok: user },
            } = await this.$http.get('/polzovateli/' + username);
            this.user = user;
        } catch (e) {
            this.$toasted.error(e.response.data.err);
        }
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
