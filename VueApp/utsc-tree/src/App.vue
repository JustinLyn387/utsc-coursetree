<template>
  <v-app>

    <LoginModal/>

    <v-app-bar app>
      <v-img
        class="logo"
        src="https://upload.wikimedia.org/wikipedia/en/thumb/0/04/Utoronto_coa.svg/1200px-Utoronto_coa.svg.png"
        aspect-ratio="1"
        max-width="50"
        max-height="50"
        v-on:click="$router.push('/')"
      />
      <v-toolbar-title class="headline" v-on:click="$router.push('/')">
        <span>UTSC</span>
        <span class="font-weight-light"> CourseTree</span>
      </v-toolbar-title>

      <v-toolbar-items>
        <navbar/>
      </v-toolbar-items>
      <v-spacer/>
      <v-toolbar-items>
        <!-- Login Button -->
        <button v-if="!this.$store.state.user.loggedIn" class="loginButton" v-on:click="openLoginModal()">{{ this.$store.state.user.displayName }}</button>
        <button v-else class="loginButton">{{ this.$store.state.user.displayName }}</button>
        <!-- Dropdown menu for settings -->
        <v-menu transition="slide-y-transition" :offset-y="true" bottom>
          <template v-slot:activator="{ on }">
            <v-btn class="settingsIcon" v-on="on" color="primary"><font-awesome-icon :icon="['fas', 'bars']" size="2x"/></v-btn>
          </template>
          <v-list>
            <v-list-item v-for="(item, i) in userOptions" :key="i" @click="executeOptions(item.page)">
              <v-list-item-title class="popupMenu">{{ item.option }}</v-list-item-title>
            </v-list-item>
          </v-list>

        </v-menu>

      </v-toolbar-items>
    </v-app-bar>

    <v-content>
      <router-view/>
    </v-content>

  </v-app>

</template>

<script>

import NavBar from './components/NavBar.vue'
import LoginModal from './components/LoginModal'
import firebase from 'firebase'

export default {
  name: 'App',
  components: {
    LoginModal,
    'navbar': NavBar
  },
  data: () => ({
    allOptions: [
      { option: 'Admin Panel', page: '/admin', access: 3 },
      { option: 'User Dashboard', page: '/dashboard', access: 1 },
      { option: 'Feedback & Updates', page: '/feedback', access: 0 },
      { option: 'About Us', page: '/about', access: 0 },
      { option: 'Logout', page: 'logout', access: 1 }
    ]
  }),
  computed: {
    // compute available options based on the users access level
    userOptions () {
      return this.allOptions.filter(option => {
        if (option.access <= this.$store.state.user.access) {
          return option
        }
      })
    }
  },
  methods: {
    logout () {
      firebase.auth().signOut().then(() => {
        if (this.$route.name !== 'home') {
          this.$router.push('/')
        } else {
          location.reload()
        }
        this.$store.commit('setUserState', false)
      })
    },
    openLoginModal () {
      // Reset store error values
      this.$store.commit('resetAuthError')
      // Open the modal
      this.$modal.show('loginPopup')
    },
    executeOptions (option) {
      // Determine if navigating to new page or logging out
      if (option !== 'logout') {
        this.$router.push(option)
      } else {
        this.logout()
      }
    }
  }
}
</script>

<style scoped>
  .settingsIcon{
    align-self: center;
    padding-left: 18px;
  }
  .loginButton{
    padding-right: 30px;
    font-size: 21px;
    color: royalblue;
    font-weight: bold;
    outline: none;
  }
  .headline:hover{
    cursor: pointer;
  }
  .logo:hover{
    cursor: pointer;
  }
  .popupMenu{
    font-size: 17px;
  }
</style>
