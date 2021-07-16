<template>
  <v-container fluid justify-center fill-height>
    <v-layout align-center justify-center>
      <v-card>
        <v-form ref="form" v-model="valid" lazy-validation class="pa-4">
          <v-card-title primary-title>
            <div>
              <h3 class="headline mb-0">Create club</h3>
            </div>
          </v-card-title>
          <v-card-text
            >Enter a name and username for the new club below.
          </v-card-text>
          <v-divider class="mt-3 mb-5"></v-divider>
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
            v-model="nameClub"
            class="ma-2"
            label="Clubname"
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
  name: 'AddClubComponent',
  data: function() {
    return {
      imageClub: 'http://localhost:5000/api/image/defaultteam.png',
      nameClub: null,
      valid: true,
      file: null,
      nameRules: [
        v => !!v || 'Clubname is required',
        v => (v && v.length > 1) || 'Clubname must be longer than 1 character',
      ],
    }
  },
  beforeCreate() {
    this.$store.commit('setNav', true)
  },
  methods: {
    submit() {
      if (this.$refs.form.validate()) {
        let formData = new FormData()
        formData.append('name', this.nameClub)
        formData.append('image', this.file)
        axios
          .post('/api/club', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
          })
          .then(() => {
            this.$store.dispatch('getAllClubs')
            this.$router.push('/home')
          })
          .catch(error => {
            console.log(error)
            this.$store.commit('setErrorDialog', {
              show: true,
              message: 'This club already exists.',
            })
          })
      }
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
