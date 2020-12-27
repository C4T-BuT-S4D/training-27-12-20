<template>
    <div>
        <form class="form" @submit.prevent="accTrade">
            <input
                type="text"
                v-model="form.кого"
                placeholder="кого"
                class="input"
            />
            <input
                type="text"
                v-model="form.отКого"
                placeholder="отКого"
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
                кого: '',
                отКого: '',
            },
        };
    },

    methods: {
        accTrade: async function() {
            try {
                await this.$http.post('/torg/prinyat', this.form);
                await this.$store.dispatch('UPDATE_USER');
                this.$router.push({ name: 'me' });
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
