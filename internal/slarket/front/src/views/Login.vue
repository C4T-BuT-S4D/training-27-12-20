<template>
    <div>
        <form class="form" @submit.prevent="login">
            <input
                type="text"
                v-model="form.ктоНахуй"
                placeholder="ктоНахуй"
                class="input"
            />
            <input
                type="text"
                v-model="form.пароль"
                placeholder="пароль"
                class="input"
            />
            <input type="submit" value="Submit" class="input" />
        </form>
    </div>
</template>

<script>
export default {
    data: function() {
        return {
            form: {
                ктоНахуй: '',
                пароль: '',
            },
        };
    },

    methods: {
        login: async function() {
            try {
                await this.$http.post('/login', this.form);
                await this.$store.dispatch('UPDATE_USER');
                this.$router.push({ name: 'index' });
            } catch (e) {
                this.$toasted.error(e.response.data.err);
            }
        },
    },
};
</script>

<style lang="scss" scoped>
.form {
    border: 1px solid black;

    width: 60%;
    margin: auto;

    display: flex;
    flex-flow: column;

    .input {
        display: block;
        margin: 1em;
        height: 2em;
    }
}
</style>
