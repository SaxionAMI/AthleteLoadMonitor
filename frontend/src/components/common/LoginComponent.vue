<template>
  <v-main>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card class="elevation-12">
            <v-toolbar dark class="toolbar">
              <v-toolbar-title>Login</v-toolbar-title>
              <v-spacer></v-spacer>
            </v-toolbar>
            <v-form ref="form">
              <v-card-text>
                <v-text-field
                  v-model="email"
                  required
                  :rules="fieldRule"
                  prepend-icon="person"
                  name="login"
                  label="Email"
                  type="text"
                  @keyup.enter="login"
                ></v-text-field>
                <v-text-field
                  id="password"
                  v-model="password"
                  required
                  :rules="fieldRule"
                  prepend-icon="lock"
                  :append-icon="showPassword ? 'visibility' : 'visibility_off'"
                  name="password"
                  label="Password"
                  :type="showPassword ? 'text' : 'password'"
                  @click:append="showPassword = !showPassword"
                  @keyup.enter="login"
                ></v-text-field>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn text @click="login">Login</v-btn>
              </v-card-actions>
            </v-form>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-main>
</template>

<script>
export default {
  name: 'LoginComponent',
  data: function() {
    return {
      email: '',
      password: '',
      fieldRule: [v => !!v || 'This field is required'],
      showPassword: false,
    }
  },
  beforeCreate() {
    this.$store.commit('setNav', false)
  },
  mounted() {
    if (localStorage.getItem('JWT') !== null) {
      this.$store.commit('setJWT', localStorage.getItem('JWT'))
      this.$router.push('/home')
    }
  },

  methods: {
    login: function() {
      if (this.$refs.form.validate()) {
        this.$store.dispatch('login', {
          email: this.email,
          password: this.password,
        })
      }
    },
  },
}
</script>

<style lang="scss">
.toolbar {
  background: $color-nav;
}
</style>
