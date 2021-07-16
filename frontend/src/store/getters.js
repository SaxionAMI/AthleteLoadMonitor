export default {
  getJWT: state => {
    return state.JWT
  },
  navEnabeled: state => {
    return state.ui.showNav
  },
  getRole: state => {
    return state.user.role
  },
  getUserId: state => {
    return state.user._id
  },
  getClubs: state => {
    return state.clubs
  },
  getSelectedClub: state => {
    return state.ui.selectedClub
  },
  getTeams: state => {
    return state.teams
  },
  getSelectedTeam: state => {
    return state.ui.selectedTeam
  },
  getImportDialog: state => {
    return state.importDialog
  },
  getNewClubDialog: state => {
    return state.newClubDialog
  },
  getNewTrainerDialog: state => {
    return state.newTrainerDialog
  },
  getNewTeamDialog: state => {
    return state.newTeamDialog
  },
  getNewPlayerDialog: state => {
    return state.newPlayerDialog
  },
  getErrorDialog: state => {
    return state.errorDialog
  },
}
