<template>
  <v-container class="my-3">
    <h1>Training Import</h1>
    <br />
    <v-layout v-if="configurations.length > 0">
      <v-flex>
        <import-card-component
          v-for="configuration in configurations"
          :key="configuration._id"
          :configuration="configuration"
        ></import-card-component>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import axios from 'axios'
import ImportCardComponent from '@/components/import/ImportCardComponent'

export default {
  name: 'Import',
  components: { ImportCardComponent },
  data() {
    return {
      configurations: [],
    }
  },
  mounted() {
    this.getAllConfigurations()
  },
  methods: {
    getAllConfigurations() {
      axios.get('/api/import/configuration/all').then(res => {
        this.configurations = res.data
      })
    },
  },
}
</script>

<style scoped></style>
