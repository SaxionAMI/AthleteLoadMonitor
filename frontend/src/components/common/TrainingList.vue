<template>
  <v-container class="my-5">
    <p class="display-1">{{ player.name }}</p>
    <v-expansion-panels v-if="trainings.length > 0" popout>
      <v-expansion-panel v-for="training in trainings" :key="training.name">
        <v-expansion-panel-header>
          <v-layout row wrap :class="`pa-3 player ${setRisk(training)}`">
            <v-flex xs6 sm3 lg3>
              <div class="caption grey--text">Date</div>
              <div>{{ formatDate(training.timestamp) }}</div>
            </v-flex>
            <v-flex xs2 sm3 lg3>
              <div class="caption grey--text">Duration</div>
              <div>{{ training.recorded_duration }}</div>
            </v-flex>
            <v-flex xs6 sm3 lg3>
              <div class="caption grey--text">RPE</div>
              <div>{{ training['rpe'] }}</div>
            </v-flex>
            <v-flex xs2 sm3 lg2>
              <div class="caption grey--text">Risk</div>
              <v-chip
                small
                :class="`${setRisk(training)} white--text caption my-2`"
              >
                {{ setRisk(training) }}
              </v-chip>
            </v-flex>
          </v-layout>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-card>
            <v-card-text>
              <v-layout wrap justify-center align-center>
                <v-flex xs12 sm6 d-flex>
                  <v-select
                    v-model="dropdownItem"
                    :items="dropdownItems"
                    label="Physical condition"
                    :menu-props="{ zIndex: '1000' }"
                    :item-text="'label'"
                    return-object
                    @change="changeChart"
                  ></v-select>
                </v-flex>

                <chart-bar
                  :key="componentKey"
                  :player-data="player"
                  :training="training"
                  :chart="dropdownItem"
                  :items="dropdownItems"
                  :averages="averages"
                ></chart-bar>
              </v-layout>
            </v-card-text>
            <v-card-actions>
              <v-layout align-center justify-center row>
                <!--                            <v-btn flat color="grey">-->
                <!--                                <v-icon small left>remove_circle</v-icon>-->
                <!--                                <span>Negeer risico</span>-->
                <!--                            </v-btn>-->
                <v-btn
                  text
                  color="grey"
                  @click="toDetailTraining(player, training, dropdownItems)"
                >
                  <v-icon small left>info</v-icon>
                  <span>Details</span>
                </v-btn>
              </v-layout>
            </v-card-actions>
          </v-card>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>

    <v-btn
      style="bottom:50px;"
      dark
      small
      absolute
      bottom
      right
      fab
      fixed
      @click="$router.push('/import')"
    >
      <v-icon>add</v-icon>
    </v-btn>
  </v-container>
</template>

<script>
import Vue from 'vue'
import moment from 'moment'
import ChartBar from './ChartBar'
import responsive from 'vue-responsive'
import axios from 'axios'

Vue.use(responsive)

export default {
  name: 'TrainingList',
  components: { ChartBar },
  props: ['player'],
  data() {
    return {
      trainings: [],
      dropdownItem: {},
      dropdownItems: [],
      componentKey: 0,
      averages: {},
    }
  },
  beforeCreate() {
    this.$store.commit('setNav', true)
  },
  created() {
    if (!this.player) {
      this.$router.push({ name: 'PlayersPerTeam' })
    }
    axios
      .get('/api/player/trainings', {
        params: { player_id: this.player._id },
      })
      .then(res => {
        axios
          .get('/api/player/averages', {
            params: { player_id: this.player._id },
          })
          .then(averages => {
            this.averages = averages.data
            this.trainings = res.data
          })
      })
    axios.get('/api/ml/configuration').then(res => {
      this.dropdownItems = res.data
    })
  },
  methods: {
    setRisk(training) {
      if (training.rpe && training.p_RPE) {
        if (Math.abs(training.rpe - training.p_RPE) > 2.5) {
          return 'high'
        } else if (Math.abs(training.rpe - training.p_RPE) > 1.5) {
          return 'medium'
        }
        return 'low'
      }
      return 'unknown'
    },
    formatDate(date) {
      return moment(date).format('DD-MM-YYYY HH:mm')
    },
    changeChart(a) {
      // quick and dirty fix
      this.dropdownItem = a
      this.componentKey += 1
    },
    toDetailTraining(player, training, list) {
      this.$router.push({
        name: 'DetailTraining',
        params: { player: player, training: training, list: list },
      })
    },
  },
}
</script>

<style scoped></style>
