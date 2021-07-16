<template>
  <v-container class="my-5">
    <h1>Trainer list</h1>
    <br />
    <v-layout v-if="trainers.length > 0" row wrap>
      <v-flex
        v-for="trainer in trainers"
        :key="trainer.username"
        xs12
        sm6
        md4
        lg3
      >
        <v-hover>
          <v-card
            slot-scope="{ hover }"
            :class="`elevation-${hover ? 12 : 2}`"
            class="text-xs-center ma-3"
          >
            <v-responsive class="pt-4">
              <v-layout align-center justify-center row fill-height>
                <v-avatar size="80px">
                  <img :src="trainer.image_url" />
                </v-avatar>
              </v-layout>
            </v-responsive>
            <v-card-text>
              <div class="grey--text">{{ trainer.email }}</div>
            </v-card-text>
            <v-card-actions>
              <v-layout column>
                <v-btn text color="grey" @click="controlTeams(trainer)">
                  <v-icon small left>build</v-icon>
                  <span>Control teams</span>
                </v-btn>
                <v-btn text color="grey" @click="showResetDialog(trainer)">
                  <v-icon small left>replay</v-icon>
                  <span>Reset password</span>
                </v-btn>
                <v-btn text color="grey" @click="showDeleteDialog(trainer)">
                  <v-icon small left>delete_sweep</v-icon>
                  <span>Delete trainer</span>
                </v-btn>
              </v-layout>
            </v-card-actions>
          </v-card>
        </v-hover>
      </v-flex>
    </v-layout>
    <v-layout v-else class="justify-center">
      <div>
        <p class="subheading">
          There are no trainers, once you add them you can find them here.
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
      @click="addOnClick"
    >
      <v-icon>add</v-icon>
    </v-btn>
    <v-dialog v-model="dialog" persistent max-width="300">
      <v-card>
        <v-responsive class="pt-4">
          <v-layout align-center justify-center row fill-height>
            <v-avatar size="80px">
              <img :src="selectedElement.image_url" />
            </v-avatar>
          </v-layout>
        </v-responsive>
        <v-card-text>
          <div class="grey--text">{{ selectedElement.email }}</div>
        </v-card-text>
        <v-card-text>
          <div>Teams</div>
        </v-card-text>
        <v-list style="max-height: 150px" class="scroll-y">
          <template v-for="team in teams">
            <v-list-tile avatar>
              <v-list-tile-content>
                <v-list-tile-title v-text="team.name"></v-list-tile-title>
              </v-list-tile-content>
              <v-btn icon>
                <v-icon
                  v-if="trainerHasTeam(team)"
                  @click="removeTeamFromTrainer(team)"
                  >check
                </v-icon>
                <v-icon v-else @click="addTrainerToTeam(team)">add</v-icon>
              </v-btn>
            </v-list-tile>
          </template>
        </v-list>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="dialog = false">
            Ok
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog
      v-model="$store.getters.getNewTrainerDialog.dialogPassword"
      persistent
      max-width="300"
    >
      <v-card>
        <v-card-text>
          We have generated new login credentials for trainer
          {{ nameTrainer }}.<br />
          Note these credentials and send them to the corresponding user.
        </v-card-text>
        <v-card-text>
          <strong>Username : </strong>
          {{ $store.getters.getNewTrainerDialog.username }}<br />
          <strong>Password : </strong>
          {{ $store.getters.getNewTrainerDialog.password }}
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            text
            @click="
              $store.commit('setNewTrainerDialog', {
                dialogPassword: false,
                username: '',
                password: '',
              })
            "
          >
            Ok
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- Dialog to reset password -->
    <v-dialog v-model="resetDialogActive" persistent max-width="290">
      <v-card>
        <div>
          <v-card-text>
            Are you sure you want to change the password for this trainer?<br />
            This action can not be reversed.
          </v-card-text>
          <v-card-actions>
            <v-btn text @click="cancelReset()">Cancel</v-btn>
            <v-spacer></v-spacer>
            <v-btn text @click="resetPassword(selectedTrainer)">
              Ok
            </v-btn>
          </v-card-actions>
        </div>
      </v-card>
    </v-dialog>
    <!-- Dialog to remove trainer -->
    <v-dialog v-model="deleteDialogActive" persistent max-width="290">
      <v-card>
        <div>
          <v-card-text>
            Are you sure you want to delete this trainer?<br />
            This action can not be reversed.
          </v-card-text>
          <v-card-actions>
            <v-btn text @click="cancelDelete()">Cancel</v-btn>
            <v-spacer></v-spacer>

            <v-btn text @click="deleteTrainer(selectedTrainer)">
              Ok
            </v-btn>
          </v-card-actions>
        </div>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TrainerList',
  data: function() {
    return {
      trainers: [],
      teams: [],
      dialog: false,
      nameTrainer: '',
      selectedElement: {},
      selectedTrainer: null,
      resetDialogActive: false,
      deleteDialogActive: false,
    }
  },
  mounted() {
    this.loadData()
  },
  beforeCreate() {
    this.$store.commit('setNav', true)
  },
  methods: {
    loadData() {
      axios.get('/api/trainer/all').then(res => (this.trainers = res.data))
    },
    addOnClick() {
      this.$router.push('/add-trainer')
    },
    controlTeams(selectedElement) {
      this.selectedElement = selectedElement
      this.getAllTeams()
      this.dialog = true
    },
    getAllTeams: function() {
      axios.get('/api/team/all').then(res => {
        this.teams = res.data
      })
    },
    trainerHasTeam(team) {
      return this.selectedElement.team_ids.includes(team._id)
    },
    addTrainerToTeam(team) {
      axios
        .put('/api/trainer/connect', null, {
          params: { user_id: this.selectedElement._id, team_id: team._id },
        })
        .then(() => {
          this.loadData()
          this.selectedElement.team_ids.push(team._id)
        })
    },
    removeTeamFromTrainer(team) {
      axios
        .put('/api/trainer/disconnect', null, {
          params: { user_id: this.selectedElement._id, team_id: team._id },
        })
        .then(() => {
          this.loadData()
          this.selectedElement.team_ids = this.selectedElement.team_ids.filter(
            teamId => teamId !== team._id
          )
        })
    },
    resetPassword(trainer) {
      axios.put('/api/trainer/reset', null, {
        params: { user_id: trainer._id },
      })
      this.selectedTrainer = null
      this.resetDialogActive = false
    },
    deleteTrainer() {
      axios
        .delete('/api/trainer', {
          params: { user_id: this.selectedTrainer['_id'] },
        })
        .then(() => this.loadData())
      this.deleteDialogActive = false
    },
    showResetDialog(trainer) {
      this.selectedTrainer = trainer
      this.resetDialogActive = true
    },
    cancelReset() {
      this.selectedTrainer = null
      this.resetDialogActive = false
    },
    showDeleteDialog(trainer) {
      this.selectedTrainer = trainer
      this.deleteDialogActive = true
    },
    cancelDelete() {
      this.selectedTrainer = null
      this.deleteDialogActive = false
    },
  },
}
</script>

<style scoped></style>
