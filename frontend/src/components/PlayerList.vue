<template>
  <v-container class="my-3">
    <h1>Player list</h1>
    <br />
    <v-layout>
      <v-flex>
        <v-expansion-panels v-if="players.length > 0">
          <v-expansion-panel
            v-for="player in players"
            :key="player.name"
            popout
            style="border:1px solid rgba(0,0,0,.12);"
            @click="getPlayerTrainings($event, player)"
          >
            <v-expansion-panel-header>
              <v-layout row wrap :class="`pa-3 player ${setRisk(player)}`">
                <v-flex xs12 sm2 md2 lg1>
                  <v-list-item-avatar>
                    <img :src="player.image_url" />
                  </v-list-item-avatar>
                </v-flex>
                <v-flex xs12 sm3 md3 lg3>
                  <div class="caption grey--text">Name</div>
                  <div>{{ player.name }}</div>
                </v-flex>
                <v-flex xs12 sm2 md3 lg3>
                  <div class="caption grey--text">Position</div>
                  <div>{{ player.position }}</div>
                </v-flex>
                <v-flex xs12 sm3 md3 lg3>
                  <div class="caption grey--text">Last training</div>
                  <div>{{ formatDate(player.latest_training) }}</div>
                </v-flex>
                <v-flex xs4 sm2 md1 lg2>
                  <div class="caption grey--text">Risk</div>
                  <v-chip
                    small
                    :class="`${setRisk(player)} white--text caption my-2 `"
                  >
                    {{ setRisk(player) }}
                  </v-chip>
                </v-flex>
              </v-layout>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-card>
                <v-card-text>
                  <v-layout
                    v-if="trainings.length !== 0"
                    wrap
                    justify-center
                    align-center
                  >
                    <v-flex xs12 sm6 d-flex>
                      <v-select
                        v-model="dropdownItem"
                        :items="dropdownItems"
                        :item-text="'label'"
                        label="Physical condition"
                        :menu-props="{ zIndex: '1000' }"
                        return-object
                        @change="changeChart"
                      ></v-select>
                    </v-flex>
                    <chart-player
                      :key="componentKey"
                      :trainings="trainings"
                      :chart-choice="dropdownItem"
                      :averages="averages"
                      :items="dropdownItems"
                    ></chart-player>
                  </v-layout>
                  <v-layout class="justify-center">
                    <div>
                      <p class="subheading">
<!--                        There's no data from this player because he has no-->
<!--                        trainings-->
                      </p>
                    </div>
                  </v-layout>
                </v-card-text>

                <v-layout>
                  <v-flex>
                    <v-card-actions>
                      <v-layout wrap justify-center>
                        <!--<v-btn flat color="grey">-->
                        <!--<v-icon small left>remove_circle</v-icon>-->
                        <!--<span>Negeer risico</span>-->
                        <!--</v-btn>-->
                        <v-btn
                          text
                          color="grey"
                          @click="settingsOnClick(player)"
                        >
                          <v-icon small left>settings</v-icon>
                          <span>Manage player</span>
                        </v-btn>
                        <v-btn
                          v-if="trainings.length !== 0"
                          text
                          color="grey"
                          @click="toTrainings(player)"
                        >
                          >
                          <v-icon small left>list</v-icon>
                          <span>Trainings</span>
                        </v-btn>
                        <v-btn
                          v-if="trainings.length !== 0"
                          text
                          color="grey"
                          @click="
                            toDetailRisico(player, setDropdownFields(player))
                          "
                        >
                          <v-icon small left>info</v-icon>
                          <span>Details</span>
                        </v-btn>
                      </v-layout>
                    </v-card-actions>
                  </v-flex>
                </v-layout>
              </v-card>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
        <v-layout v-else class="justify-center">
          <div>
            <p class="subheading">
              There are no players in this team, once you add them you can find
              find them here.
            </p>
          </div>
        </v-layout>
        <v-btn
          style="bottom:50px;"
          dark
          small
          absolute
          bottom
          right
          fab
          fixed
          @click="$router.push('/addplayer')"
        >
          <v-icon>add</v-icon>
        </v-btn>
        <v-dialog v-model="dialog" persistent max-width="400">
          <v-card>
            <v-responsive class="pt-4">
              <v-layout align-center justify-start column fill-height>
                <v-flex>
                  <v-avatar size="80px">
                    <img :src="selectedElement.image_url" />
                  </v-avatar>
                </v-flex>
              </v-layout>
            </v-responsive>
            <v-layout align-center justify-start column>
              <v-flex>
                <div class="subheading" style="text-align: center">
                  {{ selectedElement.name }}
                </div>
                <div style="text-align: center">
                  Team: {{ $store.getters.getSelectedTeam.name }}
                </div>
                <v-card-actions v-if="!selectingNewTeam">
                  <v-btn
                    text
                    outline
                    @click="selectingNewTeam = !selectingNewTeam"
                    >Select new team for this player
                  </v-btn>
                </v-card-actions>
              </v-flex>
            </v-layout>
            <v-list
              v-if="selectingNewTeam"
              style="max-height: 150px"
              class="scroll-y"
            >
              <template v-for="team in getAllTeams()">
                <v-list-tile
                  v-if="team._id !== $store.getters.getSelectedTeam._id"
                  :key="team._id"
                  avatar
                  @click="setNewTeam(team, selectedElement)"
                >
                  <v-list-tile-content>
                    <v-list-tile-title v-text="team.name"></v-list-tile-title>
                  </v-list-tile-content>
                </v-list-tile>
              </template>
            </v-list>
            <v-card-actions>
              <v-layout align-center justify-start column>
                <v-flex>
                  <v-btn text outlined @click="editPlayer(selectedElement)"
                    >Edit player
                  </v-btn>
                  <v-btn
                    text
                    outlined
                    @click="showDeleteDialog(selectedElement)"
                    >Delete this player
                  </v-btn>

                  <v-btn
                    outlined
                    text
                    @click=";(dialog = false), (selectingNewTeam = false)"
                  >
                    Ok
                  </v-btn>
                </v-flex>
              </v-layout>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <!-- Dialog to remove trainer -->
        <v-dialog v-model="deleteDialogActive" persistent max-width="290">
          <v-card>
            <div>
              <v-card-text>
                Are you sure you want to delete this player?<br />
                This action can not be reversed.
              </v-card-text>
              <v-card-actions>
                <v-btn text @click="cancelDelete()">Cancel</v-btn>
                <v-spacer></v-spacer>
                <v-btn text @click="deletePlayer(selectedPlayer)">
                  Ok
                </v-btn>
              </v-card-actions>
            </div>
          </v-card>
        </v-dialog>
        <v-dialog v-model="editPlayerDialog" persistent max-width="500">
          <v-card>
            <v-card-text>
              <v-layout align-center justify-start column fill-height>
                <v-avatar size="80px" class="text-xs-center ma-3">
                  <img id="tempImage" :src="tempEditingPlayer.image_url" />
                </v-avatar>
                <input
                  id="inputFile"
                  type="file"
                  name="imageFile"
                  class="changeimage"
                  width="inner"
                  @change="imageChanged()"
                />
                <label for="inputFile">Choose a file</label>

                <v-flex>
                  <v-select
                    v-model="tempEditingPlayer.position"
                    outline
                    class="ma-2"
                    :items="possibleRatios"
                    label="Position"
                    single-line
                  >
                  </v-select>
                </v-flex>

                <v-flex xs4>
                  <v-text-field
                    v-model="tempEditingPlayer.name"
                    label="name"
                    required
                  ></v-text-field>
                </v-flex>
              </v-layout>
            </v-card-text>
            <v-card-actions>
              <v-btn text @click="onCancel">Cancel</v-btn>
              <v-spacer></v-spacer>
              <v-btn text @click="onSave">Save</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import moment from 'moment'
import ChartPlayer from './common/ChartPlayer'
import axios from 'axios'

export default {
  name: 'PlayerList',
  components: { ChartPlayer },
  data() {
    return {
      players: [],
      playertoedit: null,
      dropdownItem: null,
      selectedElement: {},
      dialog: false,
      selectingNewTeam: false,
      editPlayerDialog: false,
      componentKey: 0,
      possibleRatios: ['Goalkeeper', 'Defender', 'Striker', 'Midfielder'],
      tempEditingPlayer: {},
      file: null,
      selectedPlayer: null,
      deleteDialogActive: false,
      trainings: [],
      averages: [],
      dropdownItems: [],
    }
  },
  computed: {
    currentTeam() {
      return this.$store.getters.getSelectedTeam
    },
  },
  watch: {
    currentTeam() {
      this.loadPlayers()
    },
  },
  beforeCreate() {
    this.$store.commit('setNav', true)
  },
  mounted() {
    this.loadPlayers()
    axios.get('/api/ml/configuration').then(res => {
      this.dropdownItems = res.data
    })
  },
  methods: {
    editPlayer(player) {
      this.dialog = false
      this.selectedElement = player
      this.selectingNewTeam = false
      this.editPlayerDialog = true
      this.tempEditingPlayer = JSON.parse(JSON.stringify(player))
    },
    onSave() {
      let formData = new FormData()
      formData.append('name', this.tempEditingPlayer.name)
      formData.append('image', this.file)
      formData.append('position', this.tempEditingPlayer.position)
      formData.append('_id', this.tempEditingPlayer._id)
      axios
        .put('/api/player', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        })
        .then(() => this.loadPlayers())
      this.editPlayerDialog = false
      this.file = null
    },
    onCancel() {
      this.tempEditingPlayer = {}
      this.editPlayerDialog = false
      this.file = null
    },
    imageChanged() {
      var input = document.getElementById('inputFile')
      if (input.files[0].size > 1024 * 1024 * 5) {
        //5MB maximaal
        return
      }
      var fReader = new FileReader()
      fReader.readAsDataURL(input.files[0])
      fReader.onloadend = function(event) {
        this.tempEditingPlayer.image_url = event.target.result
      }.bind(this)
      this.file = input.files[0]
    },
    loadPlayers() {
      axios
        .get('/api/player/team/all', {
          params: { team_id: this.$store.getters.getSelectedTeam._id },
        })
        .then(res => {
          this.players = res.data
        })
    },

    setRisk(player) {
      if (player.risk) {
        return player.risk
      }
      return 'unknown'
    },
    formatDate(value) {
      if (value) {
        return moment(value).format('DD-MM-YYYY HH:mm')
      }
      return 'no trainings'
    },
    getPlayerTrainings(event, player) {
      this.trainings = []
      this.averages = []
      if (
        !event.currentTarget.classList.contains(
          'v-expansion-panel-header--active'
        )
      ) {
        axios
          .get('/api/player/trainings', {
            params: { player_id: player._id },
          })
          .then(res => {
            axios
              .get('/api/player/averages', {
                params: { player_id: player._id },
              })
              .then(averages => {
                this.averages = averages.data
                this.trainings = res.data
              })
          })
      }
    },
    toTrainings(player) {
      this.$router.push({
        name: 'TrainingsPerPlayer',
        params: { player: player },
      })
    },
    settingsOnClick(selectedElement) {
      this.selectedElement = selectedElement
      this.dialog = true
    },
    getAllTeams: function() {
      return this.$store.getters.getTeams
    },
    setNewTeam(team, player) {
      this.selectingNewTeam = false
      let formData = new FormData()
      formData.append('old_team_id', this.$store.getters.getSelectedTeam._id)
      formData.append('new_team_id', team._id)
      formData.append('player_id', player._id)
      axios.put('/api/player/changeTeamPlayer', formData).then(() => {
        this.loadPlayers()
        this.dialog = false
      })
    },
    showDeleteDialog(player) {
      this.deleteDialogActive = true
      this.selectedPlayer = player
    },
    deletePlayer(player) {
      axios
        .delete('/api/player', { params: { player_id: player._id } })
        .then(() => this.loadPlayers())
      this.deleteDialogActive = false
      this.selectedPlayer = null
      this.dialog = false
    },
    cancelDelete() {
      this.deleteDialogActive = false
      this.selectedPlayer = null
    },
    changeChart(a) {
      this.dropdownItem = a
      this.componentKey += 1
    },
  },
}
</script>

<style lang="scss">
.player.unknown {
  border-left: 4px solid $color-health-unknown;
}

.player.low {
  border-left: 4px solid $color-health-green;
}

.player.medium {
  border-left: 4px solid $color-health-orange;
}

.player.high {
  border-left: 4px solid $color-health-red;
}

.v-chip.unknown {
  background: $color-health-unknown !important;
}

.v-chip.low {
  background: $color-health-green !important;
}

.v-chip.medium {
  background: $color-health-orange !important;
}

.v-chip.high {
  background: $color-health-red !important;
}

.v-btn.v-btn--absolute.v-btn--bottom.v-btn--floating.v-btn--fixed.v-btn--right.v-btn--small.theme--dark {
  background: $color-floating-btn;
}

.theme--light.v-expansion-panel .v-expansion-panel__container {
  border: 1px solid rgba(0, 0, 0, 0.12) !important;
  background-color: #fff;
  color: rgba(0, 0, 0, 0.87);
}
</style>
