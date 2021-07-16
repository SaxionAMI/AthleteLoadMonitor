<template>
  <v-container fluid justify-center fill-height>
    <v-layout align-center justify-center>
      <v-card>
        <v-form ref="form" v-model="valid" lazy-validation class="pa-4">
          <v-card-title primary-title>
            <div>
              <h3 class="headline mb-0">Add club admin</h3>
            </div>
          </v-card-title>
          <v-card-text
            >Enter an email for the new club administrator below.<br />Generated
            password will be sent to the user
          </v-card-text>
          <v-divider class="mt-3 mb-5"></v-divider>
          <v-layout align-center justify-center column fill-height>
            <v-flex>
              <v-avatar size="80px" class="text-xs-center ma-3">
                <img id="tempImage" :src="imageAdmin" />
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
            :value="$store.getters.getSelectedClub.name"
            label="Team"
            required
          ></v-text-field>
          <v-text-field
            v-model="emailUser"
            class="ma-2"
            label="Email"
            :rules="nameRules"
            required
          ></v-text-field>
          <v-btn class="ma-2" @click="submit">Create</v-btn>
        </v-form>
      </v-card>
    </v-layout>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AddClubAdminComponent',
  data() {
    return {
      imageAdmin: 'http://localhost:5000/api/image/defaultavatar.png',
      emailUser: '',
      file: null,
      valid: true,
      nameRules: [
        v => !!v || 'Email is required',
        v => (v && v.length > 1) || 'Email must be longer than 1 character',
        v => /.+@.+/.test(v) || 'Invalid Email address',
      ],
    }
  },
  beforeCreate() {
    this.$store.commit('setNav', true)
  },
  mounted() {},
  methods: {
    submit() {
      let formData = new FormData()
      formData.append('email', this.emailUser)
      formData.append('club_id', this.$store.getters.getSelectedClub._id)
      formData.append('image', this.file)

      axios
        .post('/api/club/admin', formData)
        .then(() => {
          this.$router.push('/club-admin')
        })
        .catch(() => {
          this.$store.commit('setErrorDialog', {
            show: true,
            message: 'This user already exists.',
          })
        })
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
        this.imageAdmin = event.target.result
      }.bind(this)
      this.file = input.files[0]
    },
  },
}
</script>

<style scoped></style>
