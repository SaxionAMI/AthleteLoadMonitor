<template>
  <v-container>
    <v-layout>
      <v-flex>
        <v-card>
          <v-layout align-center justify-center column fill-height>
            <v-flex>
              <v-avatar size="80px" class="ma-3">
                <img :src="playData.image" />
              </v-avatar>
              <p class="text-xs-center">{{ playData.name }}</p>
            </v-flex>
            <v-flex>
              <v-container fluid grid-list>
                <v-layout row wrap>
                  <v-flex v-for="chart in listCharts" :key="chart" xl6 lg6 md6>
                    <chart-player
                      :player-data="playData"
                      :chart="chart"
                      :items="listCharts"
                    ></chart-player>
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
import ChartPlayer from './ChartPlayer'

export default {
  name: 'DetailRisico',
  components: { ChartPlayer },
  props: {
    player: {
      type: Object,
      required: true,
    },
    list: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      playData: this.player,
      listCharts: this.list,
    }
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

<style lang="scss"></style>
