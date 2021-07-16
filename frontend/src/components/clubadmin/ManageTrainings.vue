<template>
  <v-container>
    <h1>Train new machine learning model</h1>
    <v-row>
      <v-col cols="12" sm="6" md="4">
        <v-menu
          ref="st_menu"
          v-model="stMenu"
          :close-on-content-click="false"
          transition="scale-transition"
          offset-y
          min-width="auto"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="startDate"
              label="Start date"
              prepend-icon="mdi-calendar"
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker
            v-model="startDate"
            no-title
            scrollable
            @input="stMenu = false"
          >
          </v-date-picker>
        </v-menu>
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="12" sm="6" md="4">
        <v-menu
          ref="end_menu"
          v-model="endMenu"
          :close-on-content-click="false"
          transition="scale-transition"
          offset-y
          min-width="auto"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="endDate"
              label="End date"
              prepend-icon="mdi-calendar"
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker
            v-model="endDate"
            :min="startDate"
            no-title
            scrollable
            @input="endMenu = false"
          >
          </v-date-picker>
        </v-menu>
      </v-col>
      <v-col cols="12" sm="6" md="2">
        <v-checkbox label="Update existing predictions"></v-checkbox>
      </v-col>
      <v-col cols="12" sm="6" md="2">
        <v-btn @click="createNewModel()">
          Create new model
        </v-btn>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
    <h1>Unmapped player list</h1>
    <br />
    <v-layout
      v-if="unmappedPlayers.length > 0"
      fluid
      justify-center
      fill-height
    >
      <v-flex>
        <v-card class="text-xs-center ma-3">
          <template v-for="(unmappedPlayer, index) in unmappedPlayers">
            <v-hover :key="unmappedPlayer" v-slot:default="{ hover }">
              <v-list-item :class="`elevation-${hover ? 12 : 0}`">
                <v-list-item-content>
                  {{ unmappedPlayer }}
                </v-list-item-content>
                <v-list-item-action>
                  <v-flex>
                    <v-btn class="ms-3" @click="addNewPlayer(unmappedPlayer)"
                      >Add new player
                    </v-btn>
                    <v-btn
                      class="ms-3"
                      @click="openConnectionPopup(unmappedPlayer)"
                      >Connect to player
                    </v-btn>
                    <v-btn
                      class="ms-3"
                      @click="deleteRecordsOfPlayer(unmappedPlayer)"
                      >Delete records
                    </v-btn>
                  </v-flex>
                </v-list-item-action>
              </v-list-item>
            </v-hover>
            <v-divider :key="index"></v-divider>
          </template>
        </v-card>
      </v-flex>
    </v-layout>
    <v-dialog v-model="showConnectionPopup" persistent width="320">
      <v-card>
        <v-card-title>Connect {{ selectedPlayer }} to:</v-card-title>
        <v-card-text>
          <v-autocomplete
            v-model="realSelectedPlayerId"
            :items="playerList"
            item-text="name"
            item-value="_id"
            label="Select player"
          ></v-autocomplete>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="closeConnectionPopup()">Cancel</v-btn>
          <v-spacer></v-spacer>
          <v-btn
            text
            :disabled="realSelectedPlayerId === null"
            @click="connectToPlayer()"
            >Connect</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from 'axios'
import moment from 'moment'

export default {
  name: 'ManageTrainings',
  data() {
    return {
      startDate: null,
      endDate: null,
      endMenu: false,
      stMenu: false,
      unmappedPlayers: [],
      selectedPlayer: null,
      showConnectionPopup: false,
      realSelectedPlayerId: null,
      playerList: [],
    }
  },
  mounted() {
    this.getUnmappedPlayers()
    this.getRealPlayers()
  },
  methods: {
    createNewModel() {
      let stDateTimestamp = moment(this.startDate, 'YYYY-MM-DD').unix() * 1000
      let endDateTimestamp = moment(this.endDate, 'YYYY-MM-DD').unix() * 1000
      let params = {}
      if (stDateTimestamp) {
        params['start_date'] = stDateTimestamp
      }
      if (endDateTimestamp) {
        params['end_date'] = endDateTimestamp
      }
      axios.post(
        '/api/ml/train_new',
        {},
        {
          params: params,
        }
      )
    },
    getUnmappedPlayers() {
      axios.get('/api/training/management/unmapped-player/all').then(res => {
        this.unmappedPlayers = res.data
      })
    },
    getRealPlayers() {
      axios.get('/api/player/all').then(res => {
        this.playerList = res.data
      })
    },
    addNewPlayer(playerName) {
      this.$router.push({
        path: '/add-player',
        query: { playerName: playerName },
      })
    },
    openConnectionPopup(playerName) {
      this.selectedPlayer = playerName
      this.showConnectionPopup = true
    },
    closeConnectionPopup() {
      this.selectedPlayer = null
      this.showConnectionPopup = false
      this.realSelectedPlayerId = null
    },
    connectToPlayer() {
      axios
        .put('/api/player/add-name-variation', {
          player_id: this.realSelectedPlayerId,
          name: this.selectedPlayer,
        })
        .then(() => {
          this.getUnmappedPlayers()
          this.closeConnectionPopup()
        })
    },
    deleteRecordsOfPlayer(playerName) {
      axios
        .delete('/api/training/management/unmapped-player', {
          params: { player_name: playerName },
        })
        .then(() => this.getUnmappedPlayers())
    },
  },
}
</script>

<style scoped></style>
