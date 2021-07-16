<template>
  <v-dialog
    v-model="this.$store.getters.getErrorDialog.show"
    persistent
    max-width="290"
  >
    <v-card>
      <v-card-title primary-title>
        <div>
          <h3 class="headline mb-0">Something went wrong.</h3>
        </div>
      </v-card-title>
      <v-card-text>
        {{ $store.getters.getErrorDialog.message }}
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          text
          @click="$store.commit('setErrorDialog', { show: false, message: '' })"
        >
          Ok
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'ErrorDialog',
}
</script>

<style scoped></style>
