<template>
    <div id="app">
        <header>
            <span
                class="brand"
                @click="$router.push({ name: 'index' }).catch(() => {})"
                >Slarket</span
            >

            <button
                v-if="user !== null"
                class="btn sendmoney"
                @click="$router.push({ name: 'sendmoney' }).catch(() => {})"
            >
                Отправить бабосы
            </button>

            <button
                v-if="user !== null"
                class="btn acctrade"
                @click="$router.push({ name: 'acctrade' }).catch(() => {})"
            >
                Принять трейд
            </button>

            <button
                v-if="user !== null"
                class="btn catch"
                @click="$router.push({ name: 'catch' }).catch(() => {})"
            >
                Поймать
            </button>

            <button
                v-if="user !== null"
                class="btn user"
                @click="$router.push({ name: 'me' }).catch(() => {})"
            >
                {{ user.имя }}
            </button>

            <button
                class="btn login"
                @click="$router.push({ name: 'login' }).catch(() => {})"
            >
                Вход
            </button>

            <button
                class="btn register"
                @click="$router.push({ name: 'register' }).catch(() => {})"
            >
                Регистрация
            </button>
        </header>
        <main>
            <router-view />
        </main>
    </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
    computed: mapState(['user']),

    created: async function() {
        await this.$store.dispatch('UPDATE_USER');
    },
};
</script>

<style lang="scss">
body,
html {
    margin: 0;
}
</style>

<style lang="scss" scoped>
header {
    height: 4em;
    background-color: rgba(0, 0, 0, 0.551);

    display: flex;

    .brand {
        font-size: 2.3em;
        display: flex;
        flex-flow: column;
        justify-content: center;
        padding: 0.5em;
        color: white;
        cursor: pointer;
        margin-right: auto;
    }

    .btn {
        margin: 1em;

        &.sendmoney {
            background-color: rgba(237, 240, 55, 0.551);
        }

        &.acctrade {
            background-color: rgba(237, 240, 55, 0.551);
        }

        &.catch {
            background-color: rgba(237, 240, 55, 0.551);
        }

        &.user {
            background-color: rgba(44, 228, 248, 0.551);
        }

        &.login {
            background-color: rgba(70, 221, 47, 0.551);
        }

        &.register {
            background-color: rgba(226, 33, 33, 0.551);
        }
    }
}

main {
    padding: 1em;
}
</style>
