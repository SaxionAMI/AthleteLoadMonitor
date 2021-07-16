<template>
  <div>
    <div v-if="getRole() === 0">
      <clubs></clubs>
    </div>
    <div v-if="getRole() === 1">
      <teams></teams>
    </div>
    <div v-if="getRole() === 2">
      <teams></teams>
    </div>
  </div>
</template>

<script>
import Clubs from '@/components/topadmin/Clubs'
import Teams from '@/components/Teams'

export default {
  name: 'HomeComponent',
  components: { Clubs, Teams },
  beforeCreate() {
    this.$store.commit('setNav', true)
  },
  methods: {
    getRole: function() {
      return this.$store.getters.getRole
    },
  },
}
</script>

<style scoped></style>
