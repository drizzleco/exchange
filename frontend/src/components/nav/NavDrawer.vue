<template>
  <v-navigation-drawer
    v-model="$store.state.drawer"
    expand-on-hover
    app
    clipped
  >
    <v-list dense>
      <NavItem v-for="item in navLinks" :key="item.title" :item="item" link />
      <NavItem
        v-if="$store.state.loggedIn"
        @click.native="logout"
        :item="{ title: 'Logout', icon: 'mdi-logout', href: 'logout' }"
        link
      />
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import NavItem from "./NavItem";
import { eraseCookie, apiUrl } from "@/helpers";
import axios from "axios";

/**
 * Nav Drawer Component
 */
export default {
  name: "NavDrawer",
  components: {
    NavItem,
  },
  methods: {
    logout: function() {
      axios.delete(apiUrl + "/logout").then(() => {
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
};
</script>
