<template>
  <v-app-bar app clipped-left>
    <v-app-bar-nav-icon @click.stop="$store.commit('toggleDrawer')" />
    <v-toolbar-title>Exchange</v-toolbar-title>
    <v-spacer />
    <v-toolbar-title v-if="$store.state.username">
      Logged in as: {{ $store.state.username }}
    </v-toolbar-title>
  </v-app-bar>
</template>

<script>
/**
 * App Bar component
 */
export default {
  name: "AppBar",
};
</script>
