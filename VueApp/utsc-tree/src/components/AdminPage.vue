<template>
  <v-container class="adminContainer">
    <v-row>
      <!-- Left column which holds the page availability and data settings options -->
      <v-col class="leftPanels">
        <!-- Admin page title block -->
        <v-row class="rowSeparators">
          <v-card class="cardStyles">
            <h1> - Admin Panel - </h1>
            <p class="adminSubhead">Manage data, view analytics, and modify users</p>
          </v-card>
        </v-row>
        <!-- Page availability card section -->
        <v-row class="rowSeparators">
          <v-card class="cardStyles">
            <h2>Content Locks</h2>
            <p>Controls to toggle certain pages & features</p>
            <v-row><v-switch v-model="coursePageStatus" class="mx-2 pageSwitch"></v-switch><p class="switchLabels">Courses Page</p></v-row>
            <v-row><v-switch v-model="treeViewPageStatus" class="mx-2 pageSwitch"></v-switch><p class="switchLabels">TreeView Page</p></v-row>
            <v-row><v-switch v-model="infoPageStatus" class="mx-2 pageSwitch"></v-switch><p class="switchLabels">Links & Info Page</p></v-row>
            <v-row><v-switch v-model="newUsers" class="mx-2 pageSwitch"></v-switch><p class="switchLabels">Allow new users</p></v-row>
          </v-card>
        </v-row>
        <!-- Data settings card section -->
        <v-row class="rowSeparators">
          <v-card class="cardStyles">
            <h2>Data Settings</h2>
            <p>Buttons to refresh or clear stored data</p>
            <div class="buttonCluster">
              <v-btn class="mr-2 dataButtons" color="primary" v-on:click="dataButton('Reset')">Reset Analytics</v-btn>
              <v-btn class="my-2 dataButtons" color="warning" v-on:click="dataButton('Refresh')">Refresh Database</v-btn>
              <v-btn class="mr-2 dataButtons" color="red" v-on:click="dataButton('Redeploy')">Redeploy Website</v-btn>
              <v-btn class="my-2 dataButtons" color="deep-purple lighten-1" v-on:click="dataButton('Wipe')">Wipe User Data</v-btn>
              <v-btn class="mr-2 dataButtons" color="green accent-3" v-on:click="dataButton('Scan')">Scan Comments</v-btn>
              <v-btn class="my-2 dataButtons" color="pink accent-3" v-on:click="dataButton('Scan')">Idk Yet</v-btn>
            </div>
          </v-card>
        </v-row>
      </v-col>

      <!-- Right column is a container with two tabs -->
      <v-col class="rightPanels">
        <v-row class="rowSeparators">
          <v-card class="cardStyles">
            <!-- Tab sections -->
            <v-tabs background-color="transparent" color="primary" grow>
              <v-tab v-on:click="selectedTab('A')"><b>Analytics</b></v-tab>
              <v-tab v-on:click="selectedTab('U')"><b>Users</b></v-tab>
              <v-tab v-on:click="selectedTab('C')"><b>Comments</b></v-tab>
              <v-tab v-on:click="selectedTab('M')"><b>Messages</b></v-tab>
            </v-tabs>
            <!-- If they selected the analytics tab (default) -->
            <v-container class="contentContainer" v-if="this.tab==='A'">
              <v-row class="analyticsHeader">
                <h2>App Analytics</h2>
                <div class="visitButtons">
                  <v-btn small class="mx-1" color="primary">Daily</v-btn>
                  <v-btn small class="mx-1" color="warning">Weekly</v-btn>
                  <v-btn small class="mx-1" color="accent">Monthly</v-btn>
                  <v-btn small class="mx-1" color="error">Yearly</v-btn>
                </div>
              </v-row>
              <v-row>
                <v-col>
                  <h3>Page Visits</h3>
                  <v-row class="chartDivs">
                    <GChart class="charts" type="ColumnChart" :data="visitsData"/>
                  </v-row>
                  <h3>Top Used Quick Links</h3>
                  <v-row class="chartDivs">
                    <GChart class="charts" type="PieChart" :data="popularData"/>
                  </v-row>
                </v-col>
                <v-col>
                  <h3>Most Popular Treeview Courses</h3>
                  <v-row class="chartDivs">
                    <GChart class="charts" type="PieChart" :data="popularData"/>
                  </v-row>
                  <h3>Number of New Users</h3>
                  <v-row class="chartDivs">
                    <GChart class="charts" type="LineChart" :data="visitsData"/>
                  </v-row>
                </v-col>
              </v-row>
            </v-container>
            <!-- Else if they want to view the users -->
            <v-container class="contentContainer" v-else-if="this.tab==='U'">
              <!-- Using a datatable to display the user information -->
              <!-- Able to search the table and default sort is by users name -->
              <v-data-table :headers="userHeaders" :items="users" sort-by="user" :search="userSearch">
                <template v-slot:top>
                  <v-toolbar flat color="white">
                    <!-- Header section with the title and search bar -->
                    <v-toolbar-title><h3>Users</h3></v-toolbar-title>
                    <v-divider class="mx-4" inset vertical/>
                    <v-text-field class="userSearch" v-model="userSearch" label="Search for User" single-line hide-details/>
                    <!-- This is popup for when they want to edit a users details -->
                    <v-dialog v-model="dialog" max-width="500px">
                      <!-- Create the card with all the details and stuff -->
                      <v-card>
                        <v-card-title>
                          <span class="headline">User Information</span>
                        </v-card-title>
                        <v-card-text>
                          <v-container>
                            <v-row>
                              <v-col cols="12" sm="6" md="4">
                                <v-text-field v-model="editedItem.user" label="User Name"></v-text-field>
                              </v-col>
                              <v-col cols="12" sm="6" md="4">
                                <v-text-field v-model="editedItem.lvl" label="Access Level"></v-text-field>
                              </v-col>
                            </v-row>
                          </v-container>
                        </v-card-text>
                        <v-card-actions>
                          <v-spacer></v-spacer>
                          <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
                          <v-btn color="blue darken-1" text @click="save">Save</v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-dialog>

                  </v-toolbar>
                </template>
                <!-- Add in the edit and delete icons for each row in the table -->
                <template v-slot:item.action="{ item }">
                  <a class="mr-2" @click="editItem(item)"><font-awesome-icon :icon="['fa', 'edit']"/></a>
                  <a @click="deleteItem(item)"><font-awesome-icon :icon="['fa', 'trash']" color="red"/></a>
                </template>

              </v-data-table>
            </v-container>
            <!-- Else if want to look at flagged comments -->
            <v-container class="contentContainer" v-else-if="this.tab==='C'">
              <v-data-table :headers="commentHeaders" :items="userComments" sort-by="date" :search="commentSearch">
                <template v-slot:top>
                  <v-toolbar flat color="white">
                    <!-- Header section with the title and search bar -->
                    <v-toolbar-title><h3>User Comments</h3></v-toolbar-title>
                    <v-divider class="mx-4" inset vertical/>
                    <v-text-field class="userSearch" v-model="commentSearch" label="Search for comments" single-line hide-details/>
                  </v-toolbar>
                </template>
                <!-- Add in the edit and delete icons for each row in the table -->
                <template v-slot:item.action="{ item }">

                  <v-menu transition="slide-y-transition" :offset-y="true" bottom>
                    <template v-slot:activator="{ on }">
                      <v-btn small class="settingsIcon" v-on="on" color="red accent-3">Action</v-btn>
                    </template>
                    <v-list>
                      <v-list-item v-for="(option, i) in settingsOptions" :key="i" @click="commentAction(option.action, item)">
                        <v-list-item-title class="popupMenu">{{ option.option }}</v-list-item-title>
                      </v-list-item>
                    </v-list>

                  </v-menu>
                </template>
              </v-data-table>
            </v-container>
            <!-- Else want to view message dashboard -->
            <v-container class="contentContainer" v-else>
              <h2>Developer Messages & Updates Dashboard</h2>
              <v-container class="pt-6">
                <h3>Add new message or announcement</h3>
                <v-text-field label="Title" v-model="message.messageTitle"></v-text-field>
                <v-textarea auto-grow clearable label="Type message or announcement" rows="4" row-height="30" v-model="message.messageBody"></v-textarea>
                <v-btn class="float-right" color="primary" v-on:click="postMessage()">Add</v-btn>
              </v-container>
              <v-container class="py-12">
                <h3>Publish new update note</h3>
                <v-row>
                  <v-col cols="12" sm="6" md="4" class="pb-0">
                    <v-text-field label="Date" placeholder="MMM/YYYY" v-model="note.noteDate"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4" class="pb-0">
                    <v-select label="Type" :items="['Update', 'Bug Fix', 'Launch', 'Pilot']" v-model="note.noteType"></v-select>
                  </v-col>
                </v-row>
                <v-text-field label="Title" v-model="note.noteTitle"></v-text-field>
                <v-textarea auto-grow clearable label="Type notes" rows="4" row-height="30" v-model="note.noteBody"></v-textarea>
                <v-btn class="float-right" color="primary" v-on:click="publishNotes()">Publish</v-btn>
              </v-container>
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
import axios from 'axios'
import firebase from 'firebase'
export default {
  name: 'AdminPage',
  data: () => ({
    settingsOptions: [
      { option: 'Flag', action: 'flag' },
      { option: 'Unflag', action: 'unflag' }
    ],
    tab: 'A',
    message: { messageTitle: '', messageBody: '', date: '' },
    note: { noteTitle: '', noteBody: '', noteDate: '', noteType: '', Colour: '' },
    visitsData: [
      ['Year', 'Sales', 'Expenses', 'Profit'], ['2014', 1000, 400, 200], ['2015', 1170, 460, 250], ['2016', 660, 1120, 300], ['2017', 1030, 540, 350]
    ],
    popularData: [
      ['', ''], ['CSCA08H3', 40], ['MATA37H3', 10], ['CSCD58H3', 25], ['CSCD27H3', 20], ['LINA01H3', 5]
    ],
    dialog: false,
    userSearch: '',
    commentSearch: '',
    userHeaders: [
      { text: 'uID', value: 'uid' },
      { text: 'User', align: 'left', value: 'user' },
      { text: 'Last Login', value: 'login' },
      { text: 'Account Created', value: 'created' },
      { text: 'Actions', value: 'action', sortable: false }
    ],
    users: [],
    editedIndex: -1,
    editedItem: { user: '', lvl: '' },
    defaultItem: { user: '', lvl: '' },
    commentHeaders: [
      { text: 'ID', value: 'ID' },
      { text: 'Course', align: 'left', value: 'course' },
      { text: 'Comment', value: 'comment' },
      { text: 'User', value: 'user' },
      { text: 'Date', value: 'date' },
      { text: 'Flag', value: 'flagged' },
      { text: 'Rep', value: 'flaggedby' },
      { text: 'Actions', value: 'action', sortable: false }
    ],
    userComments: [],
    snackMessage: { activate: false, message: null, timeout: 3000 }
  }),
  created () {
    // Get the user comments from the store
    this.userComments = this.$store.state.userComments
  },
  methods: {
    // Method to toggle which container to show (Analytics or Users)
    selectedTab (tab) {
      this.tab = tab
      if (this.tab === 'U' && this.users.length === 0) {
        // Load the users from firestore
        firebase.firestore().collection('users').onSnapshot(snapshot => {
          snapshot.docs.forEach(doc => {
            let lastLogin = new Date(doc.data().lastLogin)
            let createdOn = new Date(doc.data().createdOn)
            let dummyEntry = { user: doc.data().email, uid: doc.data().uid, login: lastLogin.toString().substring(0, 24), created: createdOn.toString().substring(0, 24) }
            this.users.push(dummyEntry)
          })
        })
      }
    },
    // This method is for when they want to edit a users info. Get the index of user assign new vals and close popup
    editItem (item) {
      this.editedIndex = this.users.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },
    // This method will get the index of desired user and confirm before splicing it out
    // Will have to modify and add an API call for when deleting in the database
    deleteItem (item) {
      const index = this.users.indexOf(item)
      confirm('Are you sure you want to delete this item?') && this.users.splice(index, 1)
    },
    close () {
      this.dialog = false
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      }, 300)
    },
    // Saves the modifications made on the user
    save () {
      if (this.editedIndex > -1) {
        Object.assign(this.users[this.editedIndex], this.editedItem)
        // Check what the access level is
        if (this.editedItem.lvl === '3') {
          // Add admin to custom claim for the user
          let addAdminRole = firebase.functions().httpsCallable('addAdminRole')
          addAdminRole({ email: this.editedItem.user }).then(result => {
            this.showSnack('ADMIN role granted!')
          })
        } else if (this.editedItem.lvl === '2') {
          let addFlaggedUser = firebase.functions().httpsCallable('resetUserRole')
          addFlaggedUser({ email: this.editedItem.user }).then(result => {
            this.showSnack('User role was reset!')
          })
        } else if (this.editedItem.lvl === '1') {
          let addFlaggedUser = firebase.functions().httpsCallable('addFlaggedUser')
          addFlaggedUser({ email: this.editedItem.user }).then(result => {
            this.showSnack('User was flagged!')
          })
        }
      } else {
        this.users.push(this.editedItem)
      }
      this.close()
    },
    showSnack (message) {
      this.snackMessage.message = message
      this.snackMessage.activate = true
    },
    postMessage () {
      // Fill out the date stamp
      this.message.date = new Date().toLocaleString()
      this.$store.commit('postMessage', this.message)
      // save the message in the database
      let record = { type: 'message', data: this.message }
      axios.post('http://127.0.0.1:5000/DataPosting/record', record)
        .then(response => {
          if (response.data === 'ERROR') {
            this.showSnack('ERROR occurred!')
          } else {
            // Show snackbar confirmation
            this.showSnack('Message successfully recorded!')
          }
        })
        .catch(function () {
          this.showSnack('An error occurred!')
        })
      // reset
      this.message = { messageTitle: '', messageBody: '', date: '' }
    },
    publishNotes () {
      // determine the color based on the note type
      if (this.note.noteType === 'Launch') {
        this.note.Colour = 'primary'
      } else if (this.note.noteType === 'Update') {
        this.note.Colour = 'purple'
      } else if (this.note.noteType === 'Pilot') {
        this.note.Colour = 'cyan'
      } else {
        this.note.Colour = 'pink'
      }
      // push the message
      this.$store.commit('publishNote', this.note)
      // save the message in the database
      let record = { type: 'note', data: this.note }
      axios.post('http://127.0.0.1:5000/DataPosting/record', record)
        .then(response => {
          if (response.data === 'ERROR') {
            this.showSnack('ERROR occurred!')
          } else {
            // Show snackbar confirmation
            this.showSnack('Note successfully recorded!')
          }
        })
        .catch(function () {
          this.showSnack('An error occurred!')
        })
      // reset
      this.note = { noteTitle: '', noteBody: '', noteDate: '', noteType: '', Colour: '' }
    },
    dataButton (option) {
      if (option === 'Reset') {
        // Update the last login time in firestore
        firebase.firestore().collection('users').doc('sgFbTUeabVg1Kcj5yGUL0G0rQHJ3').update({
          lastLogin: firebase.auth().currentUser.metadata.lastSignInTime
        })
        this.showSnack('Analytics reset!')
      } else if (option === 'Refresh') {
        this.showSnack('An email will be sent once database has been refreshed!')
      } else if (option === 'Redeploy') {
        this.showSnack('Site Redeployed!')
      } else {
        this.showSnack('Deleted all users!')
      }
    },
    commentAction (action, comment) {
      let item = { comment: '' }
      let message = ''
      if (action === 'flag') {
        item = { comment: { 'ID': comment['ID'], 'action': 1, 'user': this.$store.state.user.displayName } }
        message = 'flagged!'
      } else {
        item = { comment: { 'ID': comment['ID'], 'action': 0, 'user': this.$store.state.user.displayName } }
        message = 'unflagged!'
      }
      axios.post('http://127.0.0.1:5000/DataPosting/editcomment', item)
        .then(response => {
          if (response.data === 'SUCCESS') {
            this.showSnack('Comment successfully ' + message)
          }
        })
        .catch(function () {
          this.showSnack('An error occurred!')
        })
    }
  },
  watch: {
    dialog (val) {
      val || this.close()
    }
  },
  computed: {
    coursePageStatus: {
      get () {
        return this.$store.state.coursePage
      },
      set () {
        // Update firestore value
        firebase.firestore().collection('contentLocks').doc('courseDirectory').update({
          status: !this.$store.state.coursePage
        }).then(response => {
          this.showSnack('Course Directory page toggled!')
        }).catch(e => {
          this.showSnack('ERROR Occurred: ' + e.message)
        })
      }
    },
    treeViewPageStatus: {
      get () {
        return this.$store.state.treeViewPage
      },
      set () {
        // Update firestore value
        firebase.firestore().collection('contentLocks').doc('treeView').update({
          status: !this.$store.state.treeViewPage
        }).then(response => {
          this.showSnack('TreeView page toggled!')
        }).catch(e => {
          this.showSnack('ERROR Occurred: ' + e.message)
        })
      }
    },
    infoPageStatus: {
      get () {
        return this.$store.state.infoPage
      },
      set () {
        // Update firestore value
        firebase.firestore().collection('contentLocks').doc('infoLinks').update({
          status: !this.$store.state.infoPage
        }).then(response => {
          this.showSnack('Info & Links page toggled!')
        }).catch(e => {
          this.showSnack('ERROR Occurred: ' + e.message)
        })
      }
    },
    newUsers: {
      get () {
        return this.$store.state.newUsers
      },
      set () {
        // Update firestore value
        firebase.firestore().collection('contentLocks').doc('newUsers').update({
          status: !this.$store.state.newUsers
        }).then(response => {
          this.showSnack('New users function toggled!')
        }).catch(e => {
          this.showSnack('ERROR Occurred: ' + e.message)
        })
      }
    }
  }
}
</script>

<style scoped>
  h1{
    text-align: center;
  }
  .cardStyles{
    padding: 15px;
    width: 100%;
  }
  .leftPanels{
    max-width: 25%;
  }
  .rightPanels{
    max-width: 75%;
    padding-left: 10px;
    padding-right: 10px;
  }
  .rowSeparators{
    padding: 0 10px 20px;
  }
  .chartDivs{
    max-width: 100%;
    height: 300px;
  }
  .charts{
    width: 100%;
    height: 100%;
  }
  .visitButtons{
    margin-left: 20px;
    margin-top: 3px;
  }
  .userSearch{
    max-width: 30%;
    float: right;
  }
  .adminContainer{
    padding: 25px 0 0 0;
    min-width: 95%;
    min-height: 95.35vh;
    background-color: #3b5998;
  }
  .contentContainer{
    padding-bottom: 0;
    padding-top: 20px;
  }
  .analyticsHeader{
    padding-left: 12px;
    padding-top: 5px;
    padding-bottom: 5px;
  }
  .dataButtons{
    width: 185px;
    color: white;
  }
  .buttonCluster{
    text-align: center;
  }
  .adminSubhead{
    text-align: center;
    font-weight: bold;
  }
  .pageSwitch{
    margin-top: 0;
    padding-left: 10px;
  }
  .switchLabels{
    padding-top: 2px;
    font-size: 13pt;
    font-weight: bold;
  }
  .snackMessage{
    color: black;
  }
  .newUserButton{
    margin-left: 55%;
  }
</style>
