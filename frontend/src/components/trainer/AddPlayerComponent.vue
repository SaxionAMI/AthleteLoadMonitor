<template>
  <v-container fluid justify-center fill-height>
    <v-layout align-center justify-center>
      <v-card>
        <v-form ref="form" v-model="valid" lazy-validation class="pa-4">
          <v-card-title primary-title>
            <div>
              <h3 class="headline mb-0">Create player</h3>
            </div>
          </v-card-title>
          <v-card-text>Enter the details of the new player below.</v-card-text>
          <v-divider class="mt-4 mb-5"></v-divider>
          <v-layout align-center justify-center column fill-height>
            <v-flex>
              <v-avatar size="80px" class="text-xs-center ma-3">
                <img id="tempImage" :src="imagePlayer" />
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
            disabled
            class="ma-2"
            :value="$store.getters.getSelectedTeam.name"
            label="Team"
            required
          ></v-text-field>
          <v-text-field
            v-model="namePlayer"
            class="ma-2"
            label="Name"
            :rules="nameRules"
            required
          ></v-text-field>
          <v-select
            v-model="selectedPos"
            outline
            class="ma-2"
            :items="positions"
            label="Position"
            single-line
          >
          </v-select>

          <v-btn class="ma-2" @click="submit">Create</v-btn>
        </v-form>
      </v-card>
    </v-layout>
    <v-dialog
      v-model="this.$store.getters.getNewPlayerDialog"
      persistent
      max-width="300"
    >
      <v-card>
        <v-card-text>
          Player '{{ namePlayer }}' has been created.<br />
        </v-card-text>
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
  name: 'AddPlayerComponent',
  data: function() {
    return {
      imagePlayer: 'http://localhost:5000/api/image/defaultavatar.png',
      file: null,
      namePlayer: null,
      valid: true,
      nameRules: [
        v => !!v || 'Name is required',
        v => (v && v.length > 1) || 'Name must be at least 1 character',
      ],
      selectedPos: 'Spits',
      positions: ['Striker', 'Midfielder', 'Defender', 'Goalkeeper'],
    }
  },
  beforeCreate() {
    this.$store.commit('setNav', true)
  },
  mounted() {
    if (this.$route.query.playerName) {
      this.namePlayer = this.$route.query.playerName
    }
  },
  methods: {
    submit: function() {
      if (this.$refs.form.validate()) {
        let formData = new FormData()
        formData.append('name', this.namePlayer)
        formData.append('position', this.selectedPos)
        formData.append('team_id', this.$store.getters.getSelectedTeam._id)
        formData.append('image', this.file)
        axios
          .post('/api/player', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
          })
          .then(() => this.$router.push('/team'))
      }
    },
    clear: function() {
      this.$refs.form.reset()
      this.$store.commit('setNewPlayerDialog', false)
      this.$router.push('/team')
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
        this.imagePlayer = event.target.result
      }.bind(this)
      this.file = input.files[0]
    },
  },
}
</script>

<style scoped></style>
