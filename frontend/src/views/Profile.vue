<template>
  <v-row align="center" justify="center">
    <v-col cols="12" sm="8" md="4">
      <h1 align="center">{{ user.username }}</h1>
      <div v-if="user.auctions.length">
        <h2>Your Auctions</h2>
        <AuctionPreview
          v-for="auction in user.auctions"
          :key="auction.id"
          :auction="auction"
        />
      </div>
      <div v-if="user.bids.length" class="my-5">
        <h2>Your Bids</h2>
        <div v-for="bid in user.bids" :key="bid.id">
          <a :href="'/auction/' + bid.auction.id" class="white">
            <h3>
              Bid for {{ bid.auction.name }} by
              {{ bid.auction.user.username }}
            </h3>
          </a>
          <Bid :bid="bid" />
        </div>
      </div>
    </v-col>
  </v-row>
</template>

<script>
import { getUser } from "@/helpers";
import Bid from "@/components/Bid";
import AuctionPreview from "@/components/AuctionPreview";

/**
 * Profile view
 * Shows you all your auctions and bids
 */
export default {
  name: "Profile",
  components: {
    AuctionPreview,
    Bid,
  },
  data: () => {
    return {
      user: {},
    };
  },
  created() {
    getUser(this.$store.state.username).then((response) => {
      this.user = response.data.data.users[0];
    });
  },
};
</script>

<style lang="scss" scoped>
a,
a > h3 {
  color: white !important;
}
</style>
