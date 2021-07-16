import Vue from 'vue'
import Router from 'vue-router'
import HomeComponent from './components/common/HomeComponent'
import AddClubComponent from './components/topadmin/AddClubComponent'
import AddTrainerComponent from './components/clubadmin/AddTrainerComponent'
import AddTeamComponent from './components/clubadmin/AddTeamComponent'
import LoginComponent from './components/common/LoginComponent'
import TrainerList from './components/clubadmin/TrainerList'
import TrainingList from './components/common/TrainingList'
import AddPlayerComponent from './components/trainer/AddPlayerComponent'
import PlayerList from './components/PlayerList'
import DetailRisico from './components/common/DetailRisico'
import DetailTraining from './components/common/DetailTraining'
import AddClubAdminComponent from '@/components/topadmin/AddClubAdminComponent'
import ClubAdminList from '@/components/topadmin/ClubAdminList'
import ImportComponent from '@/components/import/ImportComponent'
import ManageTrainings from '@/components/clubadmin/ManageTrainings'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Login',
      component: LoginComponent,
    },
    {
      path: '/home',
      name: 'Home',
      component: HomeComponent,
      beforeEnter: (to, from, next) => {
        const token = localStorage.getItem('JWT')
        if (!token) {
          next(false)
          return
        }
        const payload = atob(token.split('.')[1])
        const parsedPayload = JSON.parse(payload)

        if (parsedPayload.exp < Date.now() / 1000) {
          next(false)
        } else {
          next()
        }
      },
    },
    {
      path: '/add-club',
      name: 'Addclub',
      component: AddClubComponent,
    },
    {
      path: '/add-club-admin',
      name: 'AddClubAdmin',
      component: AddClubAdminComponent,
    },
    {
      path: '/add-trainer',
      name: 'AddTrainer',
      component: AddTrainerComponent,
    },
    {
      path: '/add-team',
      name: 'AddTeam',
      component: AddTeamComponent,
    },
    {
      path: '/add-player',
      name: 'AddPlayer',
      component: AddPlayerComponent,
    },
    {
      path: '/club-admin',
      name: 'ClubAdmin',
      component: ClubAdminList,
    },
    {
      path: '/trainers',
      name: 'Trainers',
      component: TrainerList,
    },
    {
      path: '/trainings-per-player',
      name: 'TrainingsPerPlayer',
      component: TrainingList,
      props: true,
    },
    {
      path: '/team',
      name: 'PlayersPerTeam',
      component: PlayerList,
    },
    {
      path: '/detailrisico',
      name: 'DetailRisico',
      component: DetailRisico,
      props: true,
    },
    {
      path: '/detail-training',
      name: 'DetailTraining',
      component: DetailTraining,
      props: true,
    },
    {
      path: '/import',
      name: 'ImportTrainings',
      component: ImportComponent,
      props: true,
    },
    {
      path: '/manage/trainings',
      name: 'ManageTrainings',
      component: ManageTrainings,
      props: true,
    },
    {
      path: '*',
      redirect: 'home',
    },
  ],
})
