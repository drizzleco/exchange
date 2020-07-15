<template>
  <v-card class="my-3">
    <v-card-title> ${{ bid.amount }} </v-card-title>
    <v-card-subtitle>
      Bid by: {{ bid.user.username }} at {{ formatDate(bid.created) }}
    </v-card-subtitle>
  </v-card>
</template>

<script>
import { formatDate } from "@/helpers";

export default {
  name: "Bid",
  props: ["bid"],
  methods: {
    formatDate,
  },
};
</script>
