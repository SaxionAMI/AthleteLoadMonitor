<template>
  <v-container>
    <v-layout>
      <v-flex>
        <v-card>
          <v-layout align-center justify-center column fill-height>
            <v-flex>
              <v-avatar size="80px" class="ma-3">
                <img :src="player.image" />
              </v-avatar>
              <p class="text-xs-center">{{ player.name }}</p>
            </v-flex>
            <v-flex>
              <v-container fluid grid-list>
                <v-layout row wrap>
                  <v-flex v-for="chart in list" :key="chart" xl6 lg6 md6>
                    <chart-bar
                      :player-data="player"
                      :training="training"
                      :chart="chart"
                      :items="list"
                    ></chart-bar>
                  </v-flex>
                </v-layout>
              </v-container>
            </v-flex>
          </v-layout>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import ChartBar from './ChartBar'

export default {
  name: 'DetailTraining',
  components: { ChartBar },
  props: {
    player: {
      type: Object,
      required: true,
    },
    training: {
      type: Object,
      required: true,
    },
    list: {
      type: Array,
      required: true,
    },
  },
  beforeCreate() {
    this.$store.commit('setNav', true)
  },
  mounted() {
    //lelijke hack maar geen tijd om beter te doen
    window.dispatchEvent(new Event('resize'))
  },
  created() {
    if (!this.player) {
      this.$router.push({ name: 'PlayersPerTeam' })
    }
  },
}
</script>

<style scoped></style>
