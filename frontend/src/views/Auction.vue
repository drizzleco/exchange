<template>
  <v-row align="center" justify="center">
    <v-col cols="12" sm="8" md="4">
      <AuctionPreview :auction="auction" />
      <h1 v-if="!ended">Bid on {{ this.auction.name }}:</h1>
      <v-row v-if="!ended" class="d-flex mt-3">
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
      <h1 v-if="auction.bids.length">Bids</h1>
      <Bid v-for="bid in auction.bids" :key="bid.id" :bid="bid"></Bid>
    </v-col>
  </v-row>
</template>

<script>
import { getAuction, createBid, byMostRecent } from "@/helpers";
import AuctionPreview from "@/components/AuctionPreview";
import Bid from "@/components/Bid";

/**
 * Auction view
 * Shows Auction details and a list of current Bids.
 * Allows user to bid on Auction
 */
export default {
  name: "Auction",
  components: {
    AuctionPreview,
    Bid,
  },
  data: () => {
    return {
      auction: null,
      ended: false,
      bidAmount: "",
      bidError: "",
      bidSuccess: "",
    };
  },
  methods: {
    init: function() {
      getAuction(this.$route.params.id).then((response) => {
        this.auction = response.data.data.auctions[0];
        this.auction.bids.sort(byMostRecent);
        this.checkIfEnded();
      });
    },
    handleBid: function() {
      if (!this.bidAmount) {
        this.bidError = "Please enter a bid amount";
        return;
      }
      createBid(this.$route.params.id, this.bidAmount)
        .then((response) => {
          this.bidError = response.data.errors
            ? response.data.errors[0].message
            : "";
          this.bidSuccess = response.data.data
            ? response.data.data.createBid.message
            : "";
          this.init(); // refresh
        })
        .catch((error) => {
          console.log(error);
        });
    },
    checkIfEnded() {
      if (
        new Date(this.auction.endTime + "Z").getTime() - new Date().getTime() <=
        0
      )
        this.ended = true;
    },
  },
  created() {
    this.init();
    if (!this.ended) setInterval(this.checkIfEnded, 1000);
  },
};
</script>
