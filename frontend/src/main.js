import Vue from 'vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.css'

import App from './App.vue'
import store from './store'
import router from './router'
import authInterceptor from '@/interceptors/authInterceptor'
import axios from 'axios'
import * as config from '../config'

Vue.use(Vuetify, { theme: false })
Vue.config.productionTip = false
axios.defaults.baseURL = config.apiPath

authInterceptor()

new Vue({
  vuetify: new Vuetify({
    icons: {
      iconfont: 'mdiSvg',
    },
  }),
  store,
  router,
  render: h => h(App),
}).$mount('#app')
