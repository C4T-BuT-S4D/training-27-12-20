<template>
    <div>
        <form class="form" @submit.prevent="sendMoney">
            <input
                type="text"
                v-model="form.куда"
                placeholder="куда"
                class="input"
            />
            <input
                type="number"
                v-model="form.сколько"
                placeholder="сколько"
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
                куда: '',
                сколько: '',
            },
        };
    },

    methods: {
        sendMoney: async function() {
            try {
                await this.$http.post('/babosi/otpravit', {
                    куда: this.form.куда,
                    сколько: parseInt(this.form.сколько),
                });
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
