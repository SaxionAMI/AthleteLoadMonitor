import axios from 'axios'
import router from '../router.js'
import * as config from '../../config'

//change later
var BASE_URL = config.apiPath

export default {
  login: (context, payload) => {
    axios
      .post('/api/auth/login', payload)
      .then(function(response) {
        localStorage.setItem('JWT', response.data['access_token'])
        context.commit('setJWT', response.data.token)
        router.push('/home')
        context.commit('setNav', true)
      })
      .catch(function(error) {
        console.error(error)
      })
  },
  import: (context, payload) => {
    let formData = new FormData()
    let fileKeys = Object.keys(payload)
    fileKeys.forEach(function(name) {
      formData.append(name, payload[name])
    })
    var axiosConfig = {
      method: 'POST',
      url: BASE_URL + '/api/import',
      data: formData,
      headers: {
        token: localStorage.getItem('JWT'),
        'Content-Type': 'multipart/form-data',
      },
    }
    context.commit('showImportDialog', true)
    axios(axiosConfig)
      .then(function() {
        context.commit('setImportDialogDone', true)
      })
      .catch(function(error) {
        context.commit('showImportDialog', false)
        context.commit('setErrorDialog', {
          show: true,
          message: 'Files could not be sent.',
        })
        console.error(error)
      })
  },
  editClub: (context, payload) => {
    let formData = new FormData()

    if (payload.image) {
      formData.append('file', payload.image)
    }

    let fieldsToPost = {
      oldClubName: payload.oldClubName,
      newName: payload.newClub.name,
      newZeroToTenRating: payload.newClub.zeroToTenRating,
      newInputSources: payload.newClub.inputSources,
    }

    formData.append('club', JSON.stringify(fieldsToPost))

    var axiosConfig = {
      method: 'POST',
      url: BASE_URL + '/api/club/edit',
      data: formData,
      headers: {
        token: localStorage.getItem('JWT'),
      },
    }
    axios(axiosConfig)
      .then(function() {})
      .catch(function(error) {
        console.error('test', error.response.status)
        if (error.response.status == 409) {
          context.commit('setErrorDialog', {
            show: true,
            message: 'This name already exists.',
          })
        } else {
          context.commit('setErrorDialog', {
            show: true,
            message: 'Incorrect input has been given.',
          })
        }
      })
  },
  editPlayer: function(context, payload) {
    let formData = new FormData()

    if (payload.image) {
      formData.append('file', payload.image)
    }

    let fieldsToPost = {
      oldName: payload.oldName,
      newName: payload.newName,
      position: payload.position,
    }

    formData.append('player', JSON.stringify(fieldsToPost))

    var axiosConfig = {
      method: 'POST',
      url: BASE_URL + '/api/player/edit',
      data: formData,
      headers: {
        token: localStorage.getItem('JWT'),
      },
    }
    axios(axiosConfig)
      .then(function() {})
      .catch(function(error) {
        console.error(error)
        if (error.response.status == 409) {
          context.commit('setErrorDialog', {
            show: true,
            message: 'This name already exists.',
          })
        } else {
          context.commit('setErrorDialog', {
            show: true,
            message: 'Incorrect input has been given.',
          })
        }
      })
  },
  editTeam: (context, payload) => {
    let formData = new FormData()

    if (payload.image) {
      formData.append('file', payload.image)
    }

    let fieldsToPost = {
      oldName: payload.oldName,
      newName: payload.newName,
    }

    formData.append('fields', JSON.stringify(fieldsToPost))

    var axiosConfig = {
      method: 'POST',
      url: BASE_URL + '/api/team/edit',
      data: formData,
      headers: {
        token: localStorage.getItem('JWT'),
      },
    }
    axios(axiosConfig)
      .then(function() {})
      .catch(function(error) {
        console.log(error)
        if (error.response.status === 409) {
          context.commit('setErrorDialog', {
            show: true,
            message: 'This name already exists.',
          })
        } else {
          context.commit('setErrorDialog', {
            show: true,
            message: 'Incorrect input has been given.',
          })
        }
      })
  },
  addTrainer: function(context, payload) {
    let axiosConfig = {
      method: 'POST',
      url: BASE_URL + '/api/trainer/add',
      data: { username: payload },
      headers: {
        token: localStorage.getItem('JWT'),
      },
    }
    axios(axiosConfig)
      .then(function(response) {
        response.data.dialogPassword = true
        context.commit('setNewTrainerDialog', response.data)
        context.commit('addNewTrainerLocally', response.data.trainer)
      })
      .catch(function() {
        context.commit('setErrorDialog', {
          show: true,
          message: 'This trainer could not be added, try a different name.',
        })
      })
  },
  addTeam: function(context, payload) {
    var axiosConfig = {
      method: 'POST',
      url: BASE_URL + '/api/team/add',
      data: {
        name: payload,
      },
      headers: {
        token: localStorage.getItem('JWT'),
      },
    }
    axios(axiosConfig)
      .then(function(response) {
        context.commit('setNewTeamDialog', true)
        context.commit('addNewTeamLocally', response.data)
      })
      .catch(function(error) {
        console.log(error)
        context.commit('setErrorDialog', {
          show: true,
          message: 'This team already exists.',
        })
      })
  },
  addPlayer: (context, payload) => {
    let teamName = context.getters.getSelectedTeam
    var axiosConfig = {
      method: 'POST',
      url: BASE_URL + '/api/player/add',
      data: {
        name: payload.namePlayer,
        position: payload.position,
        team: teamName,
      },
      headers: {
        token: localStorage.getItem('JWT'),
      },
    }
    axios(axiosConfig)
      .then(function(response) {
        context.commit('setNewPlayerDialog', true)
        response.data.team = teamName
        context.commit('addNewPlayerLocally', response.data)
      })
      .catch(function(error) {
        console.log(error)
        context.commit('setErrorDialog', {
          show: true,
          message: 'This player could not be added, try a different name.',
        })
      })
  },
  getAllClubs: context => {
    axios.get('/api/club/all').then(res => {
      context.commit('setClubs', res.data)
      if (res.data.length > 0) {
        context.commit('setSelectedClub', res.data[0])
      }
    })
  },
  getAllTeams: context => {
    axios.get('/api/team/all').then(res => {
      context.commit('setTeams', res.data)
      if (res.data.length > 0) {
        context.commit('setSelectedTeam', res.data[0])
      }
    })
  },

  changePassword: (context, payload) => {
    var axiosConfig = {
      method: 'POST',
      url: BASE_URL + '/api/user/edit_password',
      data: { password: payload },
      headers: { token: localStorage.getItem('JWT') },
    }
    axios(axiosConfig)
      .then(function() {
        localStorage.removeItem('JWT')
        context.commit('setJWT', null)
        context.commit('logOut')
        router.push('/')
      })
      .catch(function() {
        context.commit('setErrorDialog', {
          show: true,
          message: 'Password has not been changed.',
        })
      })
  },
  resetClubPassword: function(context, payload) {
    var axiosConfig = {
      method: 'POST',
      url: BASE_URL + '/api/club/reset_password',
      data: {
        clubname: payload,
      },
      headers: {
        token: localStorage.getItem('JWT'),
      },
    }
    axios(axiosConfig)
      .then(function(response) {
        response.data.dialogPassword = true
        context.commit('setNewClubDialog', response.data)
      })
      .catch(function() {})
  },
  deletePlayer: function(context, payload) {
    var axiosConfig = {
      method: 'POST',
      url: BASE_URL + '/api/player/delete',
      data: {
        playername: payload.name,
        teamname: context.getters.getSelectedTeam,
      },
      headers: {
        token: localStorage.getItem('JWT'),
      },
    }
    axios(axiosConfig)
      .then(function(response) {
        context.commit('deletePlayerLocally', response.data)
      })
      .catch(function(error) {
        console.log(error)
        context.commit('setErrorDialog', {
          show: true,
          message: 'User could not be removed.',
        })
      })
  },
  deleteClub: function(context, payload) {
    var axiosConfig = {
      method: 'POST',
      url: BASE_URL + '/api/club/delete',
      data: {
        clubname: payload.name,
      },
      headers: {
        token: localStorage.getItem('JWT'),
      },
    }
    axios(axiosConfig)
      .then(function(response) {
        context.commit('deleteClubLocally', response.data)
      })
      .catch(function(error) {
        console.log(error)
        context.commit('setErrorDialog', {
          show: true,
          message: 'Club could not be removed.',
        })
      })
  },
  deleteTrainer: function(context, payload) {
    var axiosConfig = {
      method: 'POST',
      url: BASE_URL + '/api/trainer/delete',
      data: {
        trainername: payload.username,
        traineremail: payload.email,
      },
      headers: {
        token: localStorage.getItem('JWT'),
      },
    }
    axios(axiosConfig)
      .then(function(response) {
        context.commit('deleteTrainerLocally', response.data)
      })
      .catch(function(error) {
        console.log(error)
        context.commit('setErrorDialog', {
          show: true,
          message: 'Trainer could not be removed.',
        })
      })
  },
  deleteTeam: function(context, payload) {
    var axiosConfig = {
      method: 'POST',
      url: BASE_URL + '/api/team/delete',
      data: {
        teamname: payload,
      },
      headers: {
        token: localStorage.getItem('JWT'),
      },
    }
    axios(axiosConfig)
      .then(function(response) {
        context.commit('deleteTeamLocally', response.data)
      })
      .catch(function() {
        context.commit('setErrorDialog', {
          show: true,
          message: 'Team could not be removed.',
        })
      })
  },
  changeTeamPlayer: function(context, payload) {
    var axiosConfig = {
      method: 'POST',
      url: BASE_URL + '/api/player/changeTeamPlayer',
      data: {
        teamname: context.getters.getSelectedTeam,
        newteamname: payload.teamname,
        playername: payload.playername.name,
      },
      headers: {
        token: localStorage.getItem('JWT'),
      },
    }
    axios(axiosConfig)
      .then(function(response) {
        context.commit('changePlayerTeam', response.data)
      })
      .catch(function(error) {
        console.log(error)
        context.commit('setErrorDialog', {
          show: true,
          message: 'Player could not switch teams.',
        })
      })
  },
  connectTeamToTrainer: function(context, payload) {
    var axiosConfig = {
      method: 'POST',
      url: BASE_URL + '/api/trainer/connectTeam',
      data: {
        trainername: payload.trainername,
        teamname: payload.teamname,
      },
      headers: {
        token: localStorage.getItem('JWT'),
      },
    }
    axios(axiosConfig)
      .then(function() {
        context.commit('addTeamToTrainer', payload)
      })
      .catch(function(error) {
        console.log(error)
      })
  },
  disconnectTeamFromTrainer: function(context, payload) {
    var axiosConfig = {
      method: 'POST',
      url: BASE_URL + '/api/trainer/disconnectTeam',
      data: {
        trainername: payload.trainername,
        teamname: payload.teamname,
      },
      headers: {
        token: localStorage.getItem('JWT'),
      },
    }
    axios(axiosConfig)
      .then(function() {
        context.commit('removeTeamFromTrainer', payload)
      })
      .catch(function(error) {
        console.log(error)
      })
  },
  resetTrainerPassword: function(context, payload) {
    var axiosConfig = {
      method: 'POST',
      url: BASE_URL + '/api/user/reset_password',
      data: {
        trainername: payload,
      },
      headers: {
        token: localStorage.getItem('JWT'),
      },
    }
    axios(axiosConfig)
      .then(function(response) {
        debugger
        response.data.dialogPassword = true
        context.commit('setNewTrainerDialog', response.data)
      })
      .catch(function(error) {
        console.log(error)
      })
  },
  updateTeam: function(context, payload) {
    var axiosConfig = {
      method: 'POST',
      url: BASE_URL + '/api/team/update_predictions',
      data: {
        team: payload,
      },
      headers: {
        token: localStorage.getItem('JWT'),
      },
    }
    axios(axiosConfig).catch(function() {
      context.commit('setErrorDialog', {
        show: true,
        message:
          "This team can't be updated at the moment, please try again later.",
      })
    })
  },
  checkPredictionVersion: function(context, payload) {
    var axiosConfig = {
      method: 'POST',
      url: BASE_URL + '/api/version',
      data: {
        versions: payload,
      },
      headers: {
        token: localStorage.getItem('JWT'),
      },
    }
    axios(axiosConfig)
      .then(function() {
        console.log('Data still up to date')
      })
      .catch(function() {})
  },
  editProfile: (context, payload) => {
    let formData = new FormData()

    if (payload.image) {
      formData.append('file', payload.image)
    }

    if (payload.password) {
      let fieldsToPost = {
        password: payload.password,
      }

      formData.append('user', JSON.stringify(fieldsToPost))
    }

    var axiosConfig = {
      method: 'POST',
      url: BASE_URL + '/api/user/edit',
      data: formData,
      headers: {
        token: localStorage.getItem('JWT'),
      },
    }
    axios(axiosConfig)
      .then(function() {
        if (payload.password) {
          localStorage.removeItem('JWT')
          context.commit('setJWT', null)
          context.commit('logOut')
          router.push('/')
        }
      })
      .catch(function() {
        context.commit('setErrorDialog', {
          show: true,
          message: 'Incorrect input has been given.',
        })
      })
  },
}
