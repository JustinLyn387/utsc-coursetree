<template>
  <modal class="loginPopup" name="loginPopup" transition="pop-out" :width="400" :height="550">
    <v-container class="popupForm">
      <form>
        <div v-if="completeLogin">
          <h1>Hello there,<br>welcome back</h1>
          <div class="mb-4">
            <div>
              <input v-model="credentials.email" class="input" type="email" placeholder="E-mail">
            </div>
          </div>
          <div>
            <input v-model="credentials.password1" class="input" type="password" placeholder="Password"  v-on:keyup.enter="login">
          </div>
          <div>
            <p class="pt-2" v-if="this.$store.state.authError.error">{{ this.$store.state.authError.message }}</p>
          </div>

          <div v-bind:class="{'text-center': !this.$store.state.authError.error, 'textWithError': this.$store.state.authError.error}">
            <v-btn color="primary" v-on:click="login">Sign In</v-btn>
          </div>

          <div class="registerOp">
            <a class="regText">Don't have an account? </a>
            <a v-if="this.$store.state.newUsers" v-on:click="registerUser">  Sign Up!</a>
            <a v-else class="text--disabled">  Sign Up!</a>
          </div>
        </div>

        <div v-else>
          <h1>Get on board</h1>
          <div class="mb-3">
            <input v-model="credentials.email" class="input" type="email" placeholder="E-mail">
          </div>
          <div class="mb-3">
            <input v-model="credentials.password1" class="input" type="password" placeholder="Password">
          </div>
          <div>
            <input v-model="credentials.password2" class="input" type="password" placeholder="Confirm Password"  v-on:keyup.enter="signup" v-on:keyup="checkValidity">
          </div>
          <div>
            <p class="pt-2" v-if="this.$store.state.authError.error">{{ this.$store.state.authError.message }}</p>
            <p v-else></p>
          </div>

          <div v-bind:class="{'text-center': !this.$store.state.authError.error, 'textWithError': this.$store.state.authError.error}">
            <v-btn v-if="validCredentials" color="primary" v-on:click="signup">Sign Up</v-btn>
            <v-btn v-else disabled>Sign Up</v-btn>
          </div>
          <div class="registerOp">
            <a class="regText">I already have an account? </a><a v-on:click="registerUser">  Login!</a>
          </div>
        </div>

      </form>
    </v-container>
  </modal>

</template>

<script>
import firebase from 'firebase'

export default {
  name: 'LoginModal',
  data: () => ({
    completeLogin: true,
    validCredentials: false,
    credentials: { email: '', password1: '', password2: '' }
  }),
  methods: {
    registerUser () {
      this.completeLogin = !this.completeLogin
      this.$store.commit('resetAuthError')
    },
    signup () {
      // Use firebase to login the user with password and email
      firebase.auth()
        .createUserWithEmailAndPassword(this.credentials.email, this.credentials.password2)
        .then(data => {
          // Log them in after they have been created
          this.login()
          // Create firestore entry for the new user
          firebase.firestore().collection('users').doc(data.user.uid).set({
            uid: data.user.uid,
            email: data.user.email,
            createdOn: data.user.metadata.creationTime,
            lastLogin: data.user.metadata.creationTime
          })
        })
        // output error message if any
        .catch(err => {
          this.$store.state.authError.error = true
          this.$store.state.authError.message = err.message
        })
    },
    login () {
      firebase
        .auth()
        .signInWithEmailAndPassword(this.credentials.email, this.credentials.password1)
        .then(data => {
          this.$modal.hide('loginPopup')
          // Update the last login time in firestore
          firebase.firestore().collection('users').doc(data.user.uid).update({
            lastLogin: data.user.metadata.lastSignInTime
          })
        })
        // output error message if any
        .catch(err => {
          this.$store.state.authError.error = true
          this.$store.state.authError.message = err.message
        })
    },
    checkValidity () {
      this.validCredentials = this.credentials.password1 === this.credentials.password2
    }
  }
}
</script>

<style scoped>
  h1{
    color: grey;
    padding-bottom: 55px;
    padding-top: 20px;
  }
  p{
    color: red;
    font-size: 14px;
  }
  label{
    padding-right: 15px;
  }
  .popupForm{
    padding: 30px;
  }
  .loginPopup{
    border-radius: 5px;
  }
  .regText{
    color: black;
  }
  .registerOp{
    text-align: center;
    padding-top: 45px;
  }
  .text-center{
    padding-top: 55px;
  }
  .textWithError{
    text-align: center;
    padding-top: 25px;
  }
  .input {
    background-color: transparent;
    border: none;
    border-bottom: 1px solid #CCC;
    color: #555;
    font-size: 18px;
    height: 50px;
    top: 50%;
    min-width: 100%;
  }
  input:focus {
    outline: none;
  }

  input::-webkit-input-placeholder {
    color: #AAA;
  }

  input:focus::-webkit-input-placeholder {
    color: dodgerblue;
  }

  .input:focus+.underline {
    transform: scale(1);
  }

</style>
