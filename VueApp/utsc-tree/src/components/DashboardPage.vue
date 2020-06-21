<template>
  <v-container class="dashboardContainer">
    <TextSampleModal/>
    <v-row>
      <v-col class="leftColumn">
        <v-row class="rowSeparator">
          <v-card class="cardStyles">
            <div class="pageHeader">
              <h1> - Dashboard - </h1>
              <p class="dashSubhead">User overview, and manage taken courses</p>
            </div>
          </v-card>
        </v-row>
        <v-row class="rowSeparator">
          <v-card class="cardStyles">
            <h2 class="pageHeader"> - Account Info - </h2>
            <h4>Account Created:</h4>
            <h4>Access Level: {{ this.$store.state.user.access }}</h4>
            <v-btn class="deleteButton" color="error" @click="deleteAccount">Delete Account</v-btn>
          </v-card>
        </v-row>
      </v-col>
      <v-col class="rightColumn">
        <v-row class="rowSeparator">
          <v-card class="cardStyles">
            <v-tabs background-color="transparent" color="primary" grow>
              <v-tab v-on:click="switchTab('TC')"><b>Taken Courses</b></v-tab>
              <v-tab v-on:click="switchTab('CP')"><b>Planner</b></v-tab>
            </v-tabs>
            <v-container v-if="this.tab === 'CoursePlan'" class="mainContent">
              <v-col>
                <v-row>
                  <h2>Projected Graduation: SUMMER 2022</h2>
                </v-row>
                <v-row>
                  <v-col class="px-0">
                    <h3>Possible Sequencing:</h3>
                    <p>Test</p>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="px-0">
                    <h3>Progress: /20.0 Credits</h3>
                  </v-col>
                </v-row>
              </v-col>
            </v-container>
            <v-container v-else-if="this.tab === 'Taken'" class="mainContent">
              <h2>Taken Courses</h2>
              <p>In this section you can view the courses that you have completed thus far in your studies. Additionally, the courses inputted will be used to better display TreeView diagrams and courses remaining to take the desired course. To populate the table simply upload a text file of your transcript.</P>
              <v-row>
                <v-col class="infoPopColumn">
                  <font-awesome-icon v-on:click="$modal.show('textSamplePopup')" class="infoIcon" :icon="['fas', 'info-circle']"/>
                </v-col>
                <v-col class="pb-0">
                  <p><b> Instructions:</b> ACORN > Academic History > Complete Academic History > Copy and paste transcript section into a text file<br><b>Note:</b> You can filter the table by clicking on any of the column names!</p>
                </v-col>
              </v-row>
              <v-row class="mt-0">
                <v-col class="fileInput pt-0">
                  <v-file-input clearable show-size counter accept="text/*" label="Upload Transcript Text File ..." id="file" ref="file" v-on:change="handleFileUpload()"></v-file-input>
                </v-col>
                <v-col class="submitButton pt-4 pl-6">
                  <v-btn color="primary" v-on:click="submitFile()">Upload</v-btn>
                </v-col>
              </v-row>
              <v-data-table :headers="courseHeaders" :items="courses" sort-by="date"/>
            </v-container>
          </v-card>
        </v-row>
      </v-col>
    </v-row>

    <!-- Snackbar template -->
    <v-snackbar class="snackMessage" color="orange lighten-1" v-model="snackMessage.activate" :timeout="snackMessage.timeout">{{ snackMessage.message }}</v-snackbar>

  </v-container>

</template>

<script>
import TextSampleModal from './TextSampleModal'
// Import axios since using APIs to fetch and send data
import axios from 'axios'
import firebase from 'firebase'
export default {
  name: 'DashboardPage',
  components: {
    TextSampleModal
  },
  data: () => ({
    tab: 'Taken',
    file: '',
    courseHeaders: [
      { text: 'Course Code', align: 'left', value: 'code' },
      { text: 'Course Title', value: 'title' },
      { text: 'Completion Date', value: 'date' }
    ],
    courses: [
      { code: 'CSCA08H3', title: 'Computer Science', date: '2019 Fall' },
      { code: 'MATA37H3', title: 'Calculus', date: '2020 Winter' },
      { code: 'CSCD58H3', title: 'Some Computer Science Course', date: '2018 Summer' },
      { code: 'CSCD27H3', title: 'Another Computer Science Course', date: '2019 Fall' },
      { code: 'LINA01H3', title: 'Linguistics', date: '2018 Summer' },
      { code: 'CSCA08H3', title: 'Computer Science', date: '2020 Winter' },
      { code: 'CSCD58H3', title: 'Same Computer Science', date: '2020 Winter' },
      { code: 'LINA01H3', title: 'More Linguistics', date: '2019 Fall' },
      { code: 'CSCA08H3', title: 'Computer Science', date: '2018 Summer' }
    ],
    snackMessage: { activate: false, message: null, timeout: 3000 }
  }),
  methods: {
    switchTab (tab) {
      if (tab === 'CP') {
        this.tab = 'CoursePlan'
      } else if (tab === 'TC') {
        this.tab = 'Taken'
      }
    },
    submitFile () {
      let formData = new FormData()
      var transcriptFile = document.querySelector('#file')
      formData.append('transcript', transcriptFile.files[0])
      // Send the file to the server
      axios.post('http://127.0.0.1:5000/DataPosting/transcript', formData, { headers: { 'Content-Type': 'multipart/form-data' } })
        .then(response => {
          if (response.data === 'ERROR') {
            this.showSnack('INVALID File exception!')
          } else {
            this.courses = response.data
            this.showSnack('Transcript successfully uploaded!')
          }
          this.$refs.file.reset()
        })
        .catch(function () {
          this.showSnack('An error occurred!')
        })
    },
    handleFileUpload () {
      this.file = this.$refs.file.file
    },
    showSnack (message) {
      this.snackMessage.message = message
      this.snackMessage.activate = true
    },
    deleteAccount () {
      let confirmed = confirm('Are you sure you want to delete your account? This action cannot be undone...')
      if (confirmed) {
        firebase.auth().currentUser.delete().then(result => {
          // Remove db entries for the user
        })
        this.$router.push('/')
      }
    }
  }
}
</script>

<style scoped>
  .dashboardContainer{
    padding: 25px 0 0 0;
    min-width: 95%;
    background-color: cornflowerblue;
    min-height: 93.5vh;
  }
  .pageHeader{
    text-align: center;
  }
  .mainContent{
    padding-top: 20px;
  }
  .cardStyles{
    padding: 15px;
    width: 100%;
  }
  .leftColumn{
    max-width: 22%;
  }
  .rightColumn{
    max-width: 78%;
  }
  .rowSeparator{
    padding: 0 10px 20px;
  }
  .deleteButton{
    width: 100%;
  }
  .infoIcon{
    color: cornflowerblue;
  }
  .infoPopColumn{
    max-width: 16px;
  }
  .dashSubhead{
    text-align: center;
    font-weight: bold;
  }
  .fileInput{
    max-width: 85%;
  }
  .submitButton{
    max-width: 15%;
  }

</style>
