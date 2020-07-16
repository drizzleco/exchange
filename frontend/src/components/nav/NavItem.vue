<template>
  <v-list-item :to="item.href">
    <v-list-item-action>
      <v-icon>{{ item.icon }}</v-icon>
    </v-list-item-action>
    <v-list-item-content>
      <v-list-item-title>{{ item.title }}</v-list-item-title>
    </v-list-item-content>
  </v-list-item>
</template>

<script>
/**
 * Nav Item Component
 */
export default {
  name: "NavItem",
  props: ["item"],
};
</script>
