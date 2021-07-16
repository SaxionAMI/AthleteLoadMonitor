<template>
  <v-container class="my-5">
    <h1>Team list</h1>
    <br />
    <v-layout v-if="$store.getters.getTeams.length > 0" row wrap>
      <v-flex
        v-for="team in $store.getters.getTeams"
        :key="team.name"
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
            @click="cardSelected(team)"
          >
            <v-responsive class="pt-5 pb-5">
              <v-layout align-center justify-center row fill-height>
                <v-avatar size="80px">
                  <img :src="team.image_url" />
                </v-avatar>
              </v-layout>
            </v-responsive>
            <v-card-text>
              <div class="subheading">{{ team.name }}</div>
            </v-card-text>
            <v-card-actions>
              <v-layout column>
                <v-btn text color="grey" @click.stop="reloadTeam(team.name)">
                  <v-icon small left>update</v-icon>
                  <span>Update predictions</span>
                </v-btn>
                <v-btn
                  v-if="$store.getters.getRole < 2"
                  text
                  color="grey"
                  @click.stop="editTeam(team)"
                >
                  <v-icon small left>settings</v-icon>
                  <span>Edit team</span>
                </v-btn>
                <v-btn
                  v-if="$store.getters.getRole < 2"
                  text
                  color="grey"
                  @click.stop="showDeleteDialog(team)"
                >
                  <v-icon small left>delete_sweep</v-icon>
                  <span>Delete team</span>
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
          There are no teams, once you add them you can find them here.
        </p>
      </div>
    </v-layout>
    <v-btn
      v-if="$store.getters.getRole < 2"
      style="bottom:50px;"
      dark
      small
      absolute
      bottom
      right
      fab
      fixed
      @click="$router.push('/addteam')"
    >
      <v-icon>add</v-icon>
    </v-btn>

    <v-dialog v-model="updateTeamDialog" persistent max-width="290">
      <v-card>
        <v-responsive class="pt-4">
          <v-card-title primary-title>
            <div>
              <h3 class="headline mb-0">Updating team</h3>
            </div>
          </v-card-title>
          <v-card-text>
            <p class="subheading">
              Team {{ selectedTeam }} is being updated, this can take a while!
              We will update your data when ready.
            </p>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn outline text @click="updateTeamDialog = false">
              Ok
            </v-btn>
          </v-card-actions>
        </v-responsive>
      </v-card>
    </v-dialog>
    <!-- Dialog to reset password -->
    <v-dialog v-model="deleteDialogActive" persistent max-width="290">
      <v-card>
        <div>
          <v-card-text>
            Are you sure you want to delete this team?<br />
            This action can not be reversed.
          </v-card-text>
          <v-card-actions>
            <v-btn text @click="cancelDelete()">Cancel</v-btn>
            <v-spacer></v-spacer>

            <v-btn text @click="deleteTeam(selectedTeam)">
              Ok
            </v-btn>
          </v-card-actions>
        </div>
      </v-card>
    </v-dialog>
    <!-- Edit team dialog -->
    <v-dialog v-model="editTeamDialog" persistent max-width="500">
      <v-card>
        <v-card-title class="pb-0">
          <v-flex>
            <p class="title text-xs-center">Edit team</p>
          </v-flex>
        </v-card-title>
        <v-card-text>
          <v-layout align-center justify-start column fill-height>
            <v-flex>
              <v-avatar size="80px" class="text-xs-center ma-3">
                <img id="tempImage" :src="editTeamClone.image_url" />
              </v-avatar>
            </v-flex>
            <v-flex>
              <input
                id="inputFile"
                type="file"
                name="imageFile"
                class="changeimage"
                width="inner"
                @change="handleFileUpload"
              />
              <label for="inputFile">Choose a file</label>
            </v-flex>
            <v-flex class="mt-3">
              <v-text-field
                v-model="editTeamClone.name"
                required
                label="Teamname"
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
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Clubs',
  data() {
    return {
      teams: [],
      dialogPassword: false,
      button: true,
      file: null,
      selectedTeam: null,
      deleteDialogActive: false,
      oldTeamName: '',
      editTeamClone: {},
      editTeamDialog: false,
      updateTeamDialog: false,
    }
  },
  mounted() {
    this.$store.dispatch('getAllTeams')
  },
  methods: {
    deleteTeam(team) {
      axios
        .delete('/api/team', {
          params: { team_id: team['_id'] },
        })
        .then(() => {
          this.deleteDialogActive = false
          this.selectedTeam = null
          this.$store.dispatch('getAllTeams')
        })
    },
    cardSelected: function(team) {
      this.$store.commit('setSelectedTeam', team)
      this.$router.push('/team')
    },
    showDeleteDialog(team) {
      this.deleteDialogActive = true
      this.selectedTeam = team
    },
    cancelDelete() {
      this.deleteDialogActive = false
      this.selectedTeam = null
    },
    reloadTeam(team) {
      this.selectedTeam = team
      this.updateTeamDialog = true
      this.$store.dispatch('updateTeam', team)
    },
    editTeam(teamToEdit) {
      this.editTeamClone = JSON.parse(JSON.stringify(teamToEdit)) //Clone object so we don't edit the real team
      this.oldTeamName = teamToEdit.name
      this.editTeamDialog = true
    },
    handleFileUpload: function() {
      var input = document.getElementById('inputFile')
      if (input.files[0].size > 1024 * 1024 * 5) {
        //5MB maximaal
        return
      }
      var fReader = new FileReader()
      fReader.readAsDataURL(input.files[0])
      fReader.onloadend = function(event) {
        this.editTeamClone.image_url = event.target.result
      }.bind(this)
      this.file = input.files[0]
    },
    onCancel() {
      this.editTeamDialog = false
      this.file = null
      var input = document.getElementById('inputFile')
      input.value = ''
    },
    onSave() {
      let formData = new FormData()
      formData.append('name', this.editTeamClone.name)
      formData.append('image', this.file)
      formData.append('_id', this.editTeamClone._id)
      axios
        .put('/api/team', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        })
        .then(() => {
          this.$store.dispatch('getAllTeams')
        })
        .catch(() => {
          this.$store.commit('setErrorDialog', {
            show: true,
            message: 'Team with this name already exists.',
          })
        })
        .finally(() => {
          this.editTeamDialog = false
          this.file = null
        })
    },
  },
}
</script>

<style scoped></style>
