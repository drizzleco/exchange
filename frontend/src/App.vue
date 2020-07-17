<template>
  <v-app>
    <NavDrawer />
    <AppBar />
    <MainContent />
    <Footer />
  </v-app>
</template>

<script>
import NavDrawer from "@/components/nav/NavDrawer";
import AppBar from "@/components/layout/AppBar";
import MainContent from "@/components/layout/MainContent";
import Footer from "@/components/layout/Footer";
import { getCookie, cookieExists } from "@/helpers";

/**
 * Main app layout
 */
export default {
  props: {
    source: String,
  },
  components: {
    NavDrawer,
    AppBar,
    MainContent,
    Footer,
  },
  created() {
    if (cookieExists("username")) {
      this.$store.commit("setLoggedIn");
      this.$store.commit("setUsername", getCookie("username"));
    }
    this.$vuetify.theme.dark = true;
  },
};
</script>
