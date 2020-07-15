<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" expand-on-hover app clipped>
      <v-list dense>
        <v-list-item
          v-for="item in navLinks"
          :key="item.title"
          link
          :to="item.href"
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item v-if="this.$store.state.loggedIn" @click="logout">
          <v-list-item-action>
            <v-icon>mdi-logout</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Logout</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app clipped-left>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Exchange</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-title v-if="$store.state.username"
        >Logged in as: {{ $store.state.username }}</v-toolbar-title
      >
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-main>

    <v-footer app>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
import { getCookie, cookieExists, eraseCookie } from "./helpers";
import axios from "axios";
export default {
  props: {
    source: String,
  },
  data: () => ({
    drawer: null,
  }),
  methods: {
    logout: function() {
      axios.delete("http://localhost:5000/logout").then(() => {
        this.$store.commit("setLoggedOut");
        this.$store.commit("setUsername", "");
        eraseCookie("username");
        this.$router.push("/login");
      });
    },
  },
  computed: {
    navLinks: function() {
      if (this.$store.state.loggedIn)
        return [
          { title: "Home", href: "/", icon: "mdi-home-outline" },
          { title: "New Auction", href: "/new", icon: "mdi-clipboard-plus" },
          { title: "My Profile", href: "/me", icon: "mdi-account-circle" },
        ];
      else
        return [{ title: "Login/Register", href: "/login", icon: "mdi-login" }];
    },
  },
  created() {
    if (cookieExists("username") > 0) {
      this.$store.commit("setLoggedIn");
      this.$store.commit("setUsername", getCookie("username"));
    }
    this.$vuetify.theme.dark = true;
  },
};
</script>
