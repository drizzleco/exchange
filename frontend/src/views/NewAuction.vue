<template>
  <v-row align="center" justify="center">
    <v-col cols="12" sm="9" md="5">
      <v-card class="elevation-12">
        <v-toolbar color="primary" dark flat>
          <v-toolbar-title> Create an Auction</v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <v-form>
            <v-text-field
              label="Auction Name"
              name="name"
              type="text"
              v-model="name"
            ></v-text-field>

            <v-textarea
              label="Description"
              name="description"
              rows="2"
              v-model="description"
            ></v-textarea>

            <v-text-field
              v-model="price"
              type="number"
              min="0"
              step=".01"
              label="Starting Price"
            />
            <v-label>End Date</v-label>
            <v-date-picker v-model="date" landscape />
            <br />
            <v-label>End Time</v-label>
            <v-time-picker landscape scrollable v-model="time" />
          </v-form>
        </v-card-text>
        <v-card-subtitle>
          {{ message }}
        </v-card-subtitle>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="submit">Create</v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import { createAuction } from "@/helpers";

export default {
  name: "NewAuction",
  data: () => {
    return {
      name: "",
      description: "",
      price: 0.0,
      date: "",
      time: "",
      message: "",
    };
  },
  methods: {
    submit: function() {
      if (!this.date || !this.time) {
        this.message = "Please select an end date/time for your auction";
        return;
      }
      let endTime = new Date(this.date + " " + this.time).toISOString();
      let date = endTime.substring(0, 10);
      let time = endTime.substring(11, 16);
      createAuction(
        this.name,
        this.description,
        this.price,
        date + " " + time
      ).then((response) => {
        if (response.data.errors) {
          this.message = response.data.errors[0].message;
        } else {
          this.$router.push(
            "/auction/" + response.data.data.createAuction.auction.id
          );
        }
      });
    },
  },
};
</script>
