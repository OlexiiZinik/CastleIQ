<template>
  <div class="container">
    <div class="row">
      <div class="col-lg-6 offset-lg-3 col-sm-10 offset-sm-1">
        <h1 class="mt-4 text-center">Вхід</h1>
        <form class="text-center p-5" @submit.prevent="loginUser">

          <input type="text" id="username" class="form-control mb-5" placeholder="Логін" v-model="credentials.username" />
          <!-- Password -->
          <input type="password" id="password" class="form-control mb-5" placeholder="Пароль"
            v-model="credentials.password" />
          <!-- <p>
            Dont have an account? Click
            <router-link to="/register"> here </router-link> to sign up
          </p> -->
          <!-- Sign in button -->
          <!-- <center> -->
            <button class="btn btn-primary btn-block w-100 my-4" type="submit">
              Увійти
            </button>
          <!-- </center> -->
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      credentials: {
        username: "",
        password: ""
      }
    };
  },
  methods: {
    loginUser() {
      this.$store.dispatch("auth/logIn", this.credentials)
    }
  }
};
</script>