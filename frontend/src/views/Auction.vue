<template>
  <v-row align="center" justify="center">
    <v-col cols="12" sm="8" md="4">
      <h1 align="center">{{ auction.name }}</h1>
      <h2>{{ auction.description }}</h2>
      <h3>
        Created by: <strong>{{ auction.user.username }}</strong> at
        {{ formatDate(auction.created) }}
      </h3>
      <h3>Ending in: {{ formattedSecondsLeft }}</h3>
      <h3>Ends on: {{ formatDate(auction.endTime) }}</h3>
      <h3>Starting Price: ${{ auction.startingPrice }}</h3>
      <h2 class="mt-5">Bids:</h2>
      <h4>Total Bids: {{ auction.bids.length }}</h4>
      <v-row class="d-flex mt-3">
        <v-text-field
          outlined
          rounded
          clearable
          v-model="bidAmount"
          type="number"
          min="0"
          step=".01"
          :error-messages="bidError"
          :success-messages="bidSuccess"
          placeholder="Bid Amount"
        />
        <v-btn class="ma-3" @click="handleBid">Bid!</v-btn>
      </v-row>
      <Bid v-for="bid in auction.bids" :key="bid.id" :bid="bid"></Bid>
    </v-col>
  </v-row>
</template>

<script>
import { getAuction, createBid, formatSeconds, formatDate } from "@/helpers";
import Bid from "@/components/Bid";

export default {
  name: "Auction",
  components: {
    Bid,
  },
  data: () => {
    return {
      auction: null,
      secondsLeft: 1,
      formattedSecondsLeft: "",
      bidAmount: "",
      bidError: "",
      bidSuccess: "",
    };
  },
  methods: {
    init: function() {
      getAuction(this.$route.params.id).then((response) => {
        let auction = response.data.data.auctions[0];
        this.auction = auction;
        this.secondsLeft =
          (new Date(auction.endTime).getTime() - new Date().getTime()) / 1000;
        this.auction.bids.sort(function(a, b) {
          // sort bids by most recent first
          var keyA = new Date(a.created),
            keyB = new Date(b.created);
          if (keyA < keyB) return 1;
          if (keyA > keyB) return -1;
          return 0;
        });
      });
    },
    countDown: function() {
      if (this.secondsLeft > 0) {
        setTimeout(() => {
          this.secondsLeft -= 1;
          this.formattedSecondsLeft = formatSeconds(this.secondsLeft);
          this.countDown();
        }, 1000);
      }
    },
    handleBid: function() {
      if (!this.bidAmount) {
        this.bidError = "Please enter a bid amount";
        return;
      }
      createBid(this.$route.params.id, this.bidAmount)
        .then((data) => {
          this.bidError = data.data.errors ? data.data.errors[0].message : "";
          this.bidSuccess = data.data.data
            ? data.data.data.createBid.message
            : "";
          this.init(); // refresh
        })
        .catch((error) => {
          console.log(error);
        });
    },
    formatDate,
  },

  mounted() {
    this.init();
    this.countDown();
  },
};
</script>
