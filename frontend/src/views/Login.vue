<template>
  <v-row align="center" justify="center">
    <v-col cols="12" sm="8" md="4">
      <v-card class="elevation-12">
        <v-toolbar color="primary" dark flat>
          <v-toolbar-title>Login</v-toolbar-title>
        </v-toolbar>
        <v-card-subtitle>
          Don't have an account? <a href="/register">Register</a>
        </v-card-subtitle>
        <v-card-text>
          <v-form>
            <v-text-field
              label="Username"
              name="username"
              prepend-icon="mdi-account"
              type="text"
              v-model="username"
            ></v-text-field>

            <v-text-field
              id="password"
              label="Password"
              name="password"
              prepend-icon="mdi-lock"
              type="password"
              v-model="password"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-subtitle>
          {{ message }}
        </v-card-subtitle>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="submit">Login</v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import { post, setCookie, redirectIfLoggedIn } from "@/helpers";

/**
 * Login view
 */
export default {
  name: "Login",
  data: () => {
    return {
      username: "",
      password: "",
      message: "",
    };
  },
  methods: {
    submit: function() {
      post("/login", {
        username: this.username,
        password: this.password,
      })
        .then((data) => {
          let username = data.data.user.username;
          this.$store.commit("setUsername", username);
          this.$store.commit("setLoggedIn");
          setCookie("username", username, 365);
          this.$router.push("/");
        })
        .catch((error) => {
          console.log(error);
          this.message = error.response.data.message;
        });
    },
  },
  created() {
    redirectIfLoggedIn();
  },
};
</script>
