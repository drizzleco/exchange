<template>
  <v-footer app>
    <span>&copy; {{ year }}</span>
  </v-footer>
</template>

<script>
/**
 * Footer component
 */
export default {
  name: "Footer",
  data: function() {
    return {
      year: new Date().getFullYear(),
    };
  },
};
</script>
