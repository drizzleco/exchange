<template>
  <v-card class="my-3" :to="'/auction/' + auction.id">
    <v-card-title>{{ auction.name }}</v-card-title>
    <v-card-subtitle>{{ auction.description }}</v-card-subtitle>
    <v-card-text>
      <span>
        Created by: {{ auction.user.username }} at
        {{ formatDate(auction.created) }}
      </span>
      <span>Ends at: {{ formatDate(auction.endTime) }}</span>
      <span>Bids: {{ auction.bids.length }}</span>
    </v-card-text>
  </v-card>
</template>
<script>
import { formatDate } from "@/helpers";

/**
 * Auction Preview component.
 * Clicking on me brings you to the Auction view
 */
export default {
  name: "AuctionPreview",
  props: ["auction"],
  methods: {
    formatDate,
  },
};
</script>

<style lang="scss" scoped>
span {
  display: block;
}
</style>
