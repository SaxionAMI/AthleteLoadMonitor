<template>
  <v-container fluid justify-center fill-height>
    <v-layout align-center justify-center>
      <v-card>
        <v-form ref="form" v-model="valid" lazy-validation class="pa-4">
          <v-card-title primary-title>
            <div>
              <h3 class="headline mb-0">Create trainer</h3>
            </div>
          </v-card-title>
          <v-card-text
            >Enter a username for the new trainer below.<br />A new account will
            be automatically generated.
          </v-card-text>
          <v-card-text></v-card-text>
          <v-divider class="mb-5"></v-divider>
          <v-layout align-center justify-center column fill-height>
            <v-flex>
              <v-avatar size="80px" class="text-xs-center ma-3">
                <img id="tempImage" :src="imageTrainer" />
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
            v-model="emailTrainer"
            class="ma-2"
            label="Trainer email"
            :rules="emailRules"
            required
          ></v-text-field>
          <v-btn class="ma-2 jus" @click="submit">Create</v-btn>
        </v-form>
      </v-card>
    </v-layout>
    <v-dialog
      v-model="this.$store.getters.getNewTrainerDialog.dialogPassword"
      persistent
      max-width="300"
    >
      <v-card>
        <v-card-text>
          We have generated new login credentials for trainer
          {{ $store.getters.getNewTrainerDialog.username }}.<br />
          Note these credentials and send them to the corresponding user.
        </v-card-text>
        <v-card-text
          ><strong>Username : </strong
          >{{ this.$store.getters.getNewTrainerDialog.username }}<br />
          <strong>Password : </strong
          >{{ this.$store.getters.getNewTrainerDialog.password }}
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
  name: 'AddTrainerComponent',
  data: function() {
    return {
      emailTrainer: null,
      imageTrainer: 'http://localhost:5000/api/image/defaultavatar.png',
      file: null,
      valid: true,
      emailRules: [
        v => !!v || 'Name is required.',
        v => (v && v.length > 1) || 'Name must be longer than 1 character.',
        v => /.+@.+/.test(v) || 'Invalid Email address',
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
        formData.append('email', this.emailTrainer)
        formData.append('image', this.file)
        axios
          .post('/api/trainer', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
          })
          .then(() => this.$router.push('/trainers'))
      }
    },
    clear: function() {
      this.$refs.form.reset()
      this.$store.commit('setNewTrainerDialog', {
        dialogPassword: false,
        username: '',
        password: '',
      })
      this.$router.push('/trainers')
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
        this.imageTrainer = event.target.result
      }.bind(this)
      this.file = input.files[0]
    },
  },
}
</script>

<style scoped></style>
