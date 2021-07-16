<template>
  <v-container fluid justify-center fill-height>
    <v-layout align-center justify-center>
      <v-card>
        <v-form ref="form" v-model="valid" lazy-validation class="pa-4">
          <v-card-title primary-title>
            <div>
              <h3 class="headline mb-0">Create team</h3>
            </div>
          </v-card-title>
          <v-card-text
            >Enter a name for the new team below.<br />The team can be found on
            the teams overview page afterwards.
          </v-card-text>
          <v-divider class="mt-4 mb-5"></v-divider>
          <v-layout align-center justify-center column fill-height>
            <v-flex>
              <v-avatar size="80px" class="text-xs-center ma-3">
                <img id="tempImage" :src="imageClub" />
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
          </v-layout>
          <v-text-field
            v-model="nameTeam"
            class="ma-2"
            label="Team name"
            :rules="nameRules"
            required
          ></v-text-field>
          <v-btn class="ma-2" @click="submit">Create</v-btn>
        </v-form>
      </v-card>
    </v-layout>
    <v-dialog
      v-model="this.$store.getters.getNewTeamDialog"
      persistent
      max-width="300"
    >
      <v-card>
        <v-card-text> Team '{{ nameTeam }}' has been created. </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="clear">
            Ok
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AddTeamComponent',
  data: function() {
    return {
      nameTeam: null,
      imageClub: 'http://localhost:5000/api/image/defaultteam.png',
      file: null,
      valid: true,
      nameRules: [
        v => !!v || 'Teamname is required',
        v => (v && v.length > 1) || 'Teamname must be longer than 1 character',
      ],
    }
  },
  beforeCreate() {
    this.$store.commit('setNav', true)
  },
  methods: {
    submit: function() {
      if (this.$refs.form.validate()) {
        let formData = new FormData()
        formData.append('name', this.nameTeam)
        formData.append('image', this.file)
        axios.post('/api/team', formData).then(() => {
          this.$store.dispatch('getAllTeams')
          this.$router.push('/home')
        })
      }
    },
    clear: function() {
      this.$refs.form.reset()
      this.$store.commit('setNewTeamDialog', false)
      this.$router.push('/home')
    },
    handleFileUpload() {
      var input = document.getElementById('inputFile')
      if (input.files[0].size > 1024 * 1024 * 5) {
        //5MB maximaal
        return
      }
      var fReader = new FileReader()
      fReader.readAsDataURL(input.files[0])
      fReader.onloadend = function(event) {
        this.imageClub = event.target.result
      }.bind(this)
      this.file = input.files[0]
    },
  },
}
</script>

<style lang="scss"></style>
