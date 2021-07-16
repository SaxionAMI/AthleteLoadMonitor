<template>
  <div id="app">
    <v-app>
      <navigation v-if="navEnabled()"></navigation>
      <v-main>
        <router-view></router-view>
        <error-dialog></error-dialog>
      </v-main>
      <footer v-if="navEnabled()"></footer>
    </v-app>
  </div>
</template>

<script>
import Navigation from './components/nav/Navigation'
import ErrorDialog from './components/common/ErrorDialog'

export default {
  name: 'App',
  components: { ErrorDialog, Navigation },
  methods: {
    navEnabled: function() {
      return this.$store.getters.navEnabeled
    },
  },
}
</script>

<style lang="scss">
#app {
}
</style>
