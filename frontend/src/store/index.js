import Vue from 'vue'
import Vuex from 'vuex'

import actions from './actions'
import mutations from './mutations'
import getters from './getters'

Vue.use(Vuex)

export default new Vuex.Store({
  strict: process.env.NODE_ENV !== 'production',
  state: {
    JWT: null,
    role: null,
    importDialog: { show: false, percentage: 0 },
    newClubDialog: {
      dialogPassword: false,
      username: '',
      password: '',
    },
    newTrainerDialog: {
      dialogPassword: false,
      username: '',
      password: '',
    },
    newTeamDialog: false,
    newPlayerDialog: false,
    errorDialog: {
      show: false,
      message: '',
    },
    user: {},
    clubs: [],
    teams: [],
    ui: {
      menu: [],
      showNav: false,
      selectedClub: {},
      selectedTeam: {},
    },
  },
  getters,
  mutations,
  actions,
})
