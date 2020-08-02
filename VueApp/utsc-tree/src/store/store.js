import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import * as firebase from 'firebase'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: {
      loggedIn: false,
      access: 0,
      displayName: ''
    },
    authError: { error: false, message: '' },
    coursePage: false,
    treeViewPage: false,
    infoPage: false,
    newUsers: false,
    alreadyLoaded: false,
    devMessages: [],
    releaseNotes: [],
    userComments: []
  },

  mutations: {
    loadedData: (state) => {
      state.alreadyLoaded = !state.alreadyLoaded
    },
    postMessage: (state, message) => {
      state.devMessages.push(message)
    },
    publishNote: (state, note) => {
      state.releaseNotes.push(note)
    },
    loadMessages: (state, messages) => {
      state.devMessages = messages
    },
    loadNotes: (state, notes) => {
      state.releaseNotes = notes
    },
    loadComments: (state, comments) => {
      state.userComments = comments
    },
    setUserState: (state, user) => {
      if (user) {
        state.user.loggedIn = true
        state.user.displayName = user.email.substring(0, user.email.indexOf('@'))
        user.getIdTokenResult().then(idTokenResult => {
          if (idTokenResult.claims.admin) {
            state.user.access = 3
          } else if (idTokenResult.claims.flagged) {
            state.user.access = 1
          } else {
            state.user.access = 2
          }
        })
        // Update last login time
        firebase.firestore().collection('users').doc(firebase.auth().currentUser.uid).update({
          lastLogin: firebase.auth().currentUser.metadata.lastSignInTime
        }).then(response => {
          state.authError.error = false
        }).catch(err => {
          state.authError.error = true
          state.authError.message = err.message
        })
      } else {
        state.user.loggedIn = false
        state.user.access = 0
        state.user.displayName = 'Login'
      }
    },
    resetAuthError: (state) => {
      state.authError.error = false
      state.authError.message = ''
    },
    updatePageLocks: (state, data) => {
      // Access state using the id and set update the state
      state[ data.id ] = data.status
    }
  },
  actions: {
    loadStore (context) {
      if (!context.state.alreadyLoaded) {
        // axios call to load data on initial entry
        return new Promise((resolve, reject) => {
          axios.get('http://127.0.0.1:5000/DataRetrieval/dataLoad')
            .then(response => {
              // load the content locks
              // context.commit('coursePageSwitch', response.data[0][0][0] === 1)
              // context.commit('treePageSwitch', response.data[0][1][0] === 1)
              // context.commit('infoPageSwitch', response.data[0][2][0] === 1)
              // context.commit('newUsersSwitch', response.data[0][3][0] === 1)
              // load the dev messages & update notes & user comments
              context.commit('loadMessages', response.data[1])
              context.commit('loadNotes', response.data[2])
              context.commit('loadComments', response.data[3])
              // set flag so we don't keep loading new data unless refreshed the page
              context.commit('loadedData')
              resolve()
            })
            .catch((e) => {
              reject(e)
            })
        })
      }
    },
    loadLocks (context) {
      if (!context.state.alreadyLoaded) {
        return new Promise((resolve, reject) => {
          // Get the locks from firestore and update the store
          firebase.firestore().collection('contentLocks').get().then(querySnapshot => {
            querySnapshot.forEach(doc => {
              context.commit('updatePageLocks', doc.data())
            })
            // load the store
            context.dispatch('loadStore')
            resolve()
          })
            .catch((e) => {
              reject(e)
            })
        })
      }
    },
    // On auth state change we update the users status in the store
    fetchUser ({ commit }, user) {
      if (user) {
        commit('setUserState', user)
      } else {
        commit('setUserState', false)
      }
    }
  }

})
