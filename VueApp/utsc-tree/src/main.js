import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import store from './store/store.js'
import 'vue-search-select/dist/VueSearchSelect.css'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faTwitter, faFacebookSquare, faInstagram, faLinkedinIn } from '@fortawesome/free-brands-svg-icons'
import { faBars, faEdit, faTrash, faSearch, faInfoCircle } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import * as VueGoogleMaps from 'vue2-google-maps'
import VModal from 'vue-js-modal'
import VueGoogleCharts from 'vue-google-charts'
import * as firebase from 'firebase'
import VueGtag from 'vue-gtag'

library.add(faTwitter, faFacebookSquare, faInstagram, faLinkedinIn, faBars, faEdit, faTrash, faSearch, faInfoCircle)

Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.config.productionTip = false

Vue.use(VModal)

Vue.use(VueGoogleCharts)

Vue.use(VueGoogleMaps, {
  load: {
    key: process.env.VUE_APP_MAP_API_KEY,
    libraries: 'places' // necessary for places input
  }
})

const firebaseConfig = {
  apiKey: process.env.VUE_APP_FIREBASE_API_KEY,
  authDomain: 'utsc-coursetree.firebaseapp.com',
  databaseURL: 'https://utsc-coursetree.firebaseio.com',
  projectId: 'utsc-coursetree'
}
// Initialize Firebase
firebase.initializeApp(firebaseConfig)

firebase.auth().onAuthStateChanged(user => {
  store.dispatch('fetchUser', user)
})

firebase.firestore().collection('contentLocks').onSnapshot(snapshot => {
  snapshot.docs.forEach(doc => {
    store.commit('updatePageLocks', doc.data())
  })
})

Vue.use(VueGtag, {
  config: { id: process.env.VUE_APP_ANALYTICS_ID }
}, router)

new Vue({
  router,
  vuetify,
  store,
  render: h => h(App)
}).$mount('#app')
