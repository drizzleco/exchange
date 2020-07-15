<template>
  <v-row align="center" justify="center">
    <v-col cols="12" sm="8" md="4">
      <v-card class="elevation-12">
        <v-toolbar color="primary" dark flat>
          <v-toolbar-title>Register</v-toolbar-title>
        </v-toolbar>
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
              label="Email"
              name="email"
              prepend-icon="mdi-mail"
              type="email"
              v-model="email"
            ></v-text-field>
            <v-text-field
              id="password"
              label="Password"
              name="password"
              prepend-icon="mdi-lock"
              type="password"
              v-model="password"
            ></v-text-field>
            <v-text-field
              id="confirm-password"
              label="Confirm password"
              name="password"
              prepend-icon="mdi-lock"
              type="password"
              v-model="confirmPassword"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-subtitle>
          {{ message }}
        </v-card-subtitle>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="submit">Register</v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import { post } from "@/helpers";

export default {
  name: "Register",
  data: () => {
    return {
      username: "",
      email: "",
      password: "",
      confirmPassword: "",
      message: "",
    };
  },
  methods: {
    submit: function() {
      post("register", {
        username: this.username,
        email: this.email,
        password: this.password,
        confirm: this.confirmPassword,
      })
        .then((data) => {
          this.$store.commit("setUsername", data.data.user.username);
          this.$store.commit("setLoggedIn");
          this.$router.push("/");
        })
        .catch((error) => {
          console.log(error);
          this.message = error.response.data.message;
        });
    },
  },
  created() {
    if (this.$store.state.loggedIn) this.$router.push("/");
  },
};
</script>
