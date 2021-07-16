<template>
  <v-card class="ma-10">
    <v-card-title>
      <h3>{{ configuration.name }}</h3>
    </v-card-title>
    <v-card-text>
      <v-file-input
        v-model="fileInput"
        :accept="configuration.extension"
        counter
        multiple
        show-size
        small-chips
        truncate-length="50"
        placeholder="Select files"
      ></v-file-input>
    </v-card-text>
    <v-card-actions>
      <v-btn
        outlined
        text
        :disabled="fileInput.length === 0"
        @click="submitImport(configuration._id)"
      >
        Submit
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ImportCardComponent',
  props: {
    configuration: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      fileInput: [],
    }
  },
  methods: {
    submitImport() {
      let formData = new FormData()
      formData.append('configuration_id', this.configuration._id)
      this.fileInput.forEach(file => {
        formData.append('files', file)
      })
      axios.post('/api/import', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
    },
  },
}
</script>

<style scoped></style>
