<template>
  <div>
    <v-navigation-drawer v-model="drawer" fixed app>
      <v-list dense>
        <template v-for="tab in userMenuItems">
          <div :key="tab.title">
            <v-list-item @click="to(tab.path)">
              <v-list-item-action>
                <v-icon>{{ tab.icon }}</v-icon>
              </v-list-item-action>
              <v-list-item-content>
                <v-list-item-title>{{ tab.title }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-divider></v-divider>
          </div>
        </template>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar dark fixed app>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>

      <v-spacer></v-spacer>
      <v-toolbar-title v-if="getRole === 0">
        Topsport Loadmonitor
      </v-toolbar-title>
      <v-select
        v-if="$store.getters.getTeams.length > 0"
        :value="$store.getters.getSelectedTeam"
        :item-text="'name'"
        :items="$store.getters.getTeams"
        return-object
        @change="onSelectedTeamChange"
      >
      </v-select>
      <v-select
        v-else-if="$store.getters.getClubs.length > 0"
        :value="$store.getters.getSelectedClub"
        :item-text="'name'"
        :items="$store.getters.getClubs"
        return-object
        @change="onSelectedClubChange"
      >
      </v-select>
      <v-spacer></v-spacer>
      <div>{{ user.email }}</div>
      <v-menu class="text-xs-center" offset-y transition="slide-y-transition">
        <template v-slot:activator="{ on }">
          <v-avatar>
            <img
              v-if="user"
              alt="Profile pic"
              :src="user.image_url"
              v-on="on"
            />
          </v-avatar>
        </template>
        <v-list>
          <v-list-item
            v-for="menuItem in menuItems"
            :key="menuItem"
            @click="choose(menuItem)"
          >
            <v-list-item-title v-text="menuItem" />
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>
    <v-dialog v-model="dialog" persistent max-width="400">
      <v-card>
        <v-card-title class="pb-0">
          <v-flex>
            <p class="title text-xs-center">Edit profile</p>
          </v-flex>
        </v-card-title>

        <v-card-text class="py-0">
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-layout align-center justify-center column fill-height>
              <v-flex>
                <v-avatar size="80px" class="text-xs-center ma-3">
                  <img id="tempImage" :src="editedUser.image_url" />
                </v-avatar>
              </v-flex>
              <v-flex>
                <input
                  id="inputFileProfile"
                  type="file"
                  name="imageFile"
                  class="changeimage"
                  width="inner"
                  @change="handleFileUpload"
                />
                <label for="inputFileProfile">Choose a file</label>
              </v-flex>

              <v-layout align-center row fill-height>
                <v-flex xs6>
                  <label>New password:</label>
                </v-flex>
                <v-flex>
                  <v-text-field
                    v-model="password"
                    :append-icon="
                      showPassword ? 'visibility' : 'visibility_off'
                    "
                    :rules="[rules.min]"
                    :type="showPassword ? 'text' : 'password'"
                    name="input-10-1"
                    label="password"
                    hint="At least 8 characters"
                    counter
                    @click:append="showPassword = !showPassword"
                  ></v-text-field>
                </v-flex>
              </v-layout>

              <v-layout align-center row fill-height>
                <v-flex xs6>
                  <label>Repeat password:</label>
                </v-flex>
                <v-flex>
                  <v-text-field
                    v-model="repeatPassword"
                    :append-icon="
                      showPasswordRepeat ? 'visibility' : 'visibility_off'
                    "
                    :rules="[rules.min]"
                    :type="showPasswordRepeat ? 'text' : 'password'"
                    name="input-10-1"
                    label="password"
                    hint="At least 8 characters"
                    counter
                    @click:append="showPasswordRepeat = !showPasswordRepeat"
                  ></v-text-field>
                </v-flex>
              </v-layout>
              <v-flex v-if="samePasswords === false" class="ma-1">
                <v-alert
                  :value="true"
                  icon="warning"
                  outline
                  style="color: #ff1e28;"
                >
                  The passwords are not the same!
                </v-alert>
              </v-flex>
            </v-layout>
          </v-form>
        </v-card-text>
        <v-card-actions class="justify-space-between ">
          <v-btn text @click="dialog = !dialog">
            Cancel
          </v-btn>
          <v-btn text @click="onSave">
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import router from '@/router'

export default {
  name: 'Navigation',
  data: () => ({
    user: {},
    teams: [],
    editedUser: {},
    drawer: false,
    file: null,
    dialog: false,
    menuItems: ['Log out', 'Edit profile'],
    userMenuItems: [],
    valid: true,
    showPassword: false,
    showPasswordRepeat: false,
    password: '',
    repeatPassword: '',
    samePasswords: undefined,
    rules: {
      min: v => v.length >= 8 || 'At least 8 characters',
    },
    timeIntervalId: null,
  }),
  beforeCreate() {
    this.$store.commit('setNav', true)
  },
  mounted() {
    this.setUser()
    this.setMenu()
  },
  methods: {
    to: function(path) {
      this.$router.push(path)
    },
    choose: function(string) {
      if (string === 'Log out') {
        this.logout()
      } else if (string === 'Edit profile') {
        this.editedUser = JSON.parse(JSON.stringify(this.user)) //Clone object so we don't edit the real club
        this.dialog = true
      }
    },
    setMenu: function() {
      axios.get('/api/menu').then(res => {
        this.userMenuItems = res.data
      })
    },
    setUser: function() {
      axios
        .get('/api/auth/user')
        .then(res => {
          this.user = res.data
          this.$store.commit('setUser', res.data)
          if (this.user.role === 0) {
            this.$store.dispatch('getAllClubs')
          } else {
            this.$store.dispatch('getAllTeams')
          }
        })
        .catch(() => router.push('/login'))
    },
    getSelectedTeam: function() {
      return this.$store.getters.getSelectedTeam()
    },
    getRole: function() {
      return this.$store.getters.getRole
    },
    onSelectedTeamChange: function(x) {
      this.$store.commit('setSelectedTeam', x)
    },
    onSelectedClubChange: function(x) {
      this.$store.commit('setSelectedClub', x)
    },
    logout: function() {
      localStorage.removeItem('JWT')
      this.$store.commit('setJWT', null)
      this.$store.commit('logOut')
      this.$router.push('/')
    },
    handleFileUpload() {
      var input = document.getElementById('inputFileProfile')
      if (input.files[0].size > 1024 * 1024 * 5) {
        //5MB maximaal
        return
      }
      var fReader = new FileReader()
      fReader.readAsDataURL(input.files[0])
      fReader.onloadend = function(event) {
        this.editedUser.image_url = event.target.result
      }.bind(this)
      this.file = input.files[0]
    },
    onCancel() {
      this.dialog = false
      this.file = null
      var input = document.getElementById('inputFileProfile')
      input.value = ''
    },
    onSave: function() {
      if (this.password !== '') {
        if (this.password !== this.repeatPassword) {
          this.samePasswords = false
        } else {
          this.samePasswords = true

          let formData = new FormData()
          formData.append('password', this.password)
          formData.append('image', this.file)
          formData.append('user_id', this.$store.getters.getUserId)
          axios.put('/api/user', formData).then(() => this.setUser())
          this.dialog = false
        }
      } else {
        if (this.file) {
          let formData = new FormData()
          formData.append('image', this.file)
          formData.append('user_id', this.$store.getters.getUserId)
          axios.put('/api/user', formData).then(() => this.setUser())
        }
        this.dialog = false
      }
    },
  },
}
</script>

<style lang="scss">
.v-toolbar.v-toolbar--fixed.theme--dark {
  background: $color-nav;
  z-index: 10000;
}

.theme--light.v-navigation-drawer {
  z-index: 100000;
}

.theme--light.v-footer {
  z-index: 10000;
}
</style>
