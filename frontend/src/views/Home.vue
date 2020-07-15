<template>
  <Auctions />
</template>

<script>
// @ is an alias to /src
import Auctions from "@/components/Auctions.vue";

/**
 * Home view
 * You see this right after logging in or registering
 */
export default {
  name: "Home",
  components: {
    Auctions,
  },
  created() {
    if (!this.$store.state.loggedIn) this.$router.push("login");
  },
};
</script>
