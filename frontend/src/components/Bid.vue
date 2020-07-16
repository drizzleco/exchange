<template>
  <v-card class="my-3">
    <v-card-title> {{ formatMoney(bid.amount) }} </v-card-title>
    <v-card-subtitle>
      Bid by: {{ bid.user.username }} at {{ formatDate(bid.created) }}
    </v-card-subtitle>
  </v-card>
</template>

<script>
import { formatDate, formatMoney } from "@/helpers";

/**
 * Bid component
 * Displays bid amount, username, and creation date
 */
export default {
  name: "Bid",
  props: ["bid"],
  methods: {
    formatDate,
    formatMoney,
  },
};
</script>
