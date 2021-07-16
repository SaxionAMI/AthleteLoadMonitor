<template>
  <v-container class="my-5">
    <h1>Club list</h1>
    <br />
    <v-layout v-if="$store.getters.getClubs.length > 0" row wrap>
      <v-flex
        v-for="club in $store.getters.getClubs"
        :key="club.name"
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
            @click="cardSelected(club)"
          >
            <v-responsive class="pt-4">
              <v-layout align-center justify-center row fill-height>
                <v-avatar size="80px">
                  <img :src="club.image_url" />
                </v-avatar>
              </v-layout>
            </v-responsive>
            <v-card-text>
              <div class="subheading">{{ club.name }}</div>
            </v-card-text>
            <v-card-actions>
              <v-layout column>
                <v-btn text color="grey" @click.stop="editClub(club)">
                  <v-icon small left>create</v-icon>
                  <span>Edit club</span>
                </v-btn>
                <v-btn text color="grey" @click.stop="showDeleteDialog(club)">
                  <v-icon small left>delete_sweep</v-icon>
                  <span>Delete club</span>
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
          There are no clubs, once you add them you can find them here.
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
      @click="$router.push('/addclub')"
    >
      <v-icon>add</v-icon>
    </v-btn>

    <v-dialog v-model="editClubDialog" persistent max-width="500">
      <v-card>
        <v-card-title class="pb-0">
          <v-flex>
            <p class="title text-xs-center mb-0">Edit club</p>
          </v-flex>
        </v-card-title>

        <v-card-text>
          <v-layout align-center justify-center column fill-height>
            <v-flex>
              <v-avatar size="80px" class="text-xs-center ma-3">
                <img id="tempImage" :src="editClubClone.image_url" />
              </v-avatar>
            </v-flex>
            <input
              id="inputFile"
              type="file"
              name="imageFile"
              class="changeimage"
              width="inner"
              @change="handleFileUpload"
            />
            <label for="inputFile">Choose a file</label>
            <v-text-field
              v-model="editClubClone.name"
              required
              label="Clubname"
            ></v-text-field>
          </v-layout>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="onCancel">Cancel</v-btn>
          <v-spacer></v-spacer>
          <v-btn text @click="onSave">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- Dialog to remove club -->
    <v-dialog v-model="removeDialogActive" persistent max-width="290">
      <v-card>
        <div>
          <v-card-text>
            Are you sure you want to remove this club?<br />
            This action can not be reversed.
          </v-card-text>
          <v-card-actions>
            <v-btn text @click="cancelDelete()">Cancel</v-btn>
            <v-spacer></v-spacer>

            <v-btn text @click="deleteClub(selectedClub)">
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
  name: 'Clubs',
  data: function() {
    return {
      clubs: [],
      active: 0,
      file: null,
      nameClub: '',
      editClubClone: {},
      editClubDialog: false,
      removeDialogActive: false,
      resetDialogActive: false,
      selectedClub: null,
    }
  },
  mounted() {
    this.$store.dispatch('getAllClubs')
  },
  methods: {
    showDeleteDialog(club) {
      this.selectedClub = club
      this.removeDialogActive = true
    },
    deleteClub() {
      axios
        .delete('/api/club', {
          params: { club_id: this.selectedClub['_id'] },
        })
        .then(() => {
          this.$store.dispatch('getAllClubs')
        })
      this.removeDialogActive = false
    },
    cancelDelete() {
      this.selectedClub = null
      this.removeDialogActive = false
    },
    cardSelected: function(club) {
      this.$store.commit('setSelectedClub', club)
      this.$router.push('/club-admin')
    },
    showResetDialog(club) {
      this.selectedClub = club
      this.resetDialogActive = true
    },
    resetPassword(arg) {
      this.nameClub = arg.name
      this.$store.dispatch('resetClubPassword', arg.name)
      this.resetDialogActive = false
    },
    cancelReset() {
      this.selectedClub = null
      this.resetDialogActive = false
    },
    editClub(clubToEdit) {
      this.editClubClone = JSON.parse(JSON.stringify(clubToEdit)) //Clone object so we don't edit the real club
      this.editClubDialog = true
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
        this.editClubClone.image_url = event.target.result
      }.bind(this)
      this.file = input.files[0]
    },
    onCancel() {
      this.editClubDialog = false
      this.file = null
      var input = document.getElementById('inputFile')
      input.value = ''
    },
    onSave() {
      let formData = new FormData()
      formData.append('name', this.editClubClone.name)
      formData.append('image', this.file)
      formData.append('_id', this.editClubClone._id)
      axios
        .put('/api/club', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        })
        .then(() => {
          this.$store.dispatch('getAllClubs')
        })
        .catch(() => {
          this.$store.commit('setErrorDialog', {
            show: true,
            message: 'Club with this name already exists.',
          })
        })
        .finally(() => {
          this.editClubDialog = false
          this.file = null
        })
    },
    removeItem(index) {
      this.editClubClone.inputSources.splice(index, 1)
    },
  },
}
</script>

<style scoped></style>
