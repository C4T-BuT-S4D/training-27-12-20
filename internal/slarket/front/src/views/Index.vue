<template>
    <div class="masters">
        <div
            class="master"
            v-for="(user, i) of users"
            :key="i"
            @click="
                $router
                    .push({ name: 'user', params: { username: user.имя } })
                    .catch(() => {})
            "
        >
            <div>Имя: {{ user.имя }}</div>
            <div>Баланс: {{ user.баланс }}</div>
        </div>
    </div>
</template>

<script>
export default {
    data: function() {
        return {
            users: [],
        };
    },

    created: async function() {
        try {
            const {
                data: { ok: users },
            } = await this.$http.get('/polzovateli');
            this.users = users;
        } catch (e) {
            this.$toasted.error(e.response.data.err);
        }
    },
};
</script>

<style lang="scss" scoped>
.masters {
    display: flex;
    flex-flow: row wrap;

    .master {
        border: 1px solid blue;
        flex: 0 0 auto;
        margin-right: 1em;
        margin-top: 0.5em;
        padding: 0.5em;
        cursor: pointer;
    }
}
</style>
