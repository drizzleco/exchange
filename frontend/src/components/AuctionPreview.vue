<template>
  <v-card class="my-3" :to="'/auction/' + auction.id">
    <v-card-title>
      <h1>{{ auction.name }}</h1>
    </v-card-title>
    <v-card-subtitle>
      <h2>{{ auction.description }}</h2>
    </v-card-subtitle>
    <v-card-text>
      <h3>
        Created by: <strong>{{ auction.user.username }}</strong> at
        {{ formatDate(auction.created) }}
      </h3>
      <h3 v-if="!ended">Ending in: {{ formattedSecondsLeft }}</h3>
      <h3>End{{ ended ? "ed" : "s" }} on: {{ formatDate(auction.endTime) }}</h3>
      <h3 v-if="ended">
        WINNER: {{ auction.bids[0].user.username }} ({{
          formatMoney(auction.bids[0].amount)
        }})
      </h3>
      <h3>Starting Price: {{ formatMoney(auction.startingPrice) }}</h3>
      <h3>Total Bids: {{ auction.bids.length }}</h3>
    </v-card-text>
  </v-card>
</template>
<script>
import {
  formatDate,
  formatSeconds,
  formatMoney,
  byMostRecent,
} from "@/helpers";

/**
 * Auction Preview component.
 * Clicking on me brings you to the Auction view
 */
export default {
  name: "AuctionPreview",
  props: ["auction"],
  data: function() {
    return {
      secondsLeft: 1,
      formattedSecondsLeft: "",
      ended: false,
    };
  },
  methods: {
    countDown: function() {
      if (this.secondsLeft >= 1) {
        this.secondsLeft -= 1;
        this.formattedSecondsLeft = formatSeconds(this.secondsLeft);
      } else this.ended = true;
    },
    formatDate,
    formatMoney,
  },
  created() {
    this.auction.bids.sort(byMostRecent);
    let auctionEndTime = new Date(this.auction.endTime + "Z");
    this.secondsLeft = (auctionEndTime.getTime() - new Date().getTime()) / 1000;
    this.countDown();
    setInterval(this.countDown, 1000);
  },
};
</script>
