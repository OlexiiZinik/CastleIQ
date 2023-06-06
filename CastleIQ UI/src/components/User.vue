<template>
    <!-- nav-item -->
    <div class="dropdown">
        <button class="btn btn-secondary dropdown-toggle px-5" type="button" data-bs-toggle="dropdown"
            aria-expanded="false">
            {{ this.$store.state.auth.username }}
        </button>
        <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#" @click="this.$store.commit('auth/logOut')">Вийти</a></li>
        </ul>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
    data() {
        return {
            username: "user not loged in"
        }
    },
    async mounted() {
        await this.$store.dispatch("auth/getMe")
        if (!this.$store.state.auth.loggedIn) {
            this.$router.push({ name: "login" })
        }
    },
    computed: {
    }
}
</script>