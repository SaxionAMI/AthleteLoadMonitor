export default {
  setJWT: (state, token) => {
    state.JWT = token
  },
  setUser: (state, user) => {
    state.user = user
  },
  setNav: (state, payload) => {
    state.ui.showNav = payload
  },
  setRole: (state, payload) => {
    state.role = payload
  },
  showImportDialog: (state, payload) => {
    state.importDialog.show = payload
  },
  setImportDialogDone: (state, payload) => {
    state.importDialog.done = payload
  },
  setNewTeamDialog: (state, payload) => {
    state.newTeamDialog = payload
  },
  setNewPlayerDialog: (state, payload) => {
    state.newPlayerDialog = payload
  },
  setErrorDialog: (state, payload) => {
    state.errorDialog.show = payload.show
    state.errorDialog.message = payload.message
  },
  logOut: state => {
    state.JWT = null
    state.user = {}
    state.club = null
    state.clubs = []
    state.teams = []
    state.players = []
    state.trainers = []
    state.trainings = {}
    state.ui.selectedTeam = {}
    state.ui.menu = []
  },
  setSelectedClub: (state, payload) => {
    state.ui.selectedClub = payload
  },
  setClubs: (state, payload) => {
    state.clubs = payload
  },
  setSelectedTeam: (state, payload) => {
    state.ui.selectedTeam = payload
  },
  setTeams: (state, payload) => {
    state.teams = payload
  },
  addNewPlayerLocally: (state, token) => {
    state.players.push(token)
    state.trainings[token.name] = []
  },
  deletePlayerLocally: (state, payload) => {
    for (let i = 0; i < state.players.length; i++) {
      if (state.players[i].name === payload.playername) {
        state.players.splice(i, 1)
      }
    }
  },
  addNewTeamLocally: (state, token) => {
    state.teams.push(token)
    if (!state.selectedTeam) {
      state.selectedTeam = token.name
    }
  },
  addNewTrainerLocally: (state, token) => {
    state.trainers.push(token)
  },
  addNewClubLocally: (state, token) => {
    state.clubs.push(token)
  },
  addTeamToTrainer(state, payload) {
    for (let i = 0; i < state.trainers.length; i++) {
      if (payload.trainername === state.trainers[i].username) {
        state.trainers[i].teams.push(payload.teamname)
        break
      }
    }
  },
  removeTeamFromTrainer(state, payload) {
    for (let i = 0; i < state.trainers.length; i++) {
      if (payload.trainername === state.trainers[i].username) {
        state.trainers[i].teams.splice(
          state.trainers[i].teams.indexOf(payload.teamname),
          1
        )
        break
      }
    }
  },
  changePlayerTeam(state, payload) {
    for (let i = 0; i < state.players.length; i++) {
      if (state.players[i].name === payload.playername) {
        if (state.ui.selectedTeam === state.players[i].team) {
          state.players[i].team = payload.teamname
        }
      }
    }
  },
  deleteClubLocally(state, payload) {
    for (let i = 0; i < state.clubs.length; i++) {
      if (state.clubs[i].name === payload) {
        state.clubs.splice(i, 1)
        break
      }
    }
  },
  deleteTrainerLocally(state, payload) {
    for (let i = 0; i < state.trainers.length; i++) {
      if (
        state.trainers[i].username === payload.trainername &&
        state.trainers[i].email === payload.traineremail
      ) {
        state.trainers.splice(i, 1)
        break
      }
    }
  },
  deleteTeamLocally(state, payload) {
    if (state.selectedTeam === payload.name) {
      if (state.teams.length === 1) {
        state.selectedTeam = ''
      } else {
        state.selectedTeam = state.teams[0].name
      }
    }
    state.teams.splice(state.teams.indexOf(payload), 1)
  },
}
