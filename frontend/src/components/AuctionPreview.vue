<template>
  <v-card class="my-3" :to="'/auction/' + auction.id">
    <v-card-title>{{ auction.name }}</v-card-title>
    <v-card-subtitle>{{ auction.description }}</v-card-subtitle>
    <v-card-text
      >Created by: {{ auction.user.username }} at
      {{ formatDate(auction.created) }}<br />Ends at:
      {{ formatDate(auction.endTime) }}<br />Bids:
      {{ auction.bids.length }}</v-card-text
    >
  </v-card>
</template>
<script>
import { formatDate } from "@/helpers";
export default {
  name: "AuctionPreview",
  props: ["auction"],
  methods: {
    formatDate,
  },
};
</script>
