<template>
  <v-row align="center" justify="center">
    <v-col cols="12" sm="8" md="4">
      <h1 align="center">Auctions</h1>
      <AuctionPreview
        v-for="auction in auctions"
        :key="auction.id"
        :auction="auction"
      ></AuctionPreview>
    </v-col>
  </v-row>
</template>

<script>
import { getAuctions } from "@/helpers";
import AuctionPreview from "./AuctionPreview";

export default {
  name: "Auctions",
  components: {
    AuctionPreview,
  },
  data: () => {
    return {
      auctions: [],
    };
  },
  mounted() {
    getAuctions().then((response) => {
      this.auctions = response.data.data.auctions;
    });
  },
};
</script>
