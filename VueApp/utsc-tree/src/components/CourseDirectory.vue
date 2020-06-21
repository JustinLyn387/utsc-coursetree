<template>
  <!-- Container to hold the directory and course information -->
  <v-container class="container">
    <v-row >
      <v-col class="leftColumn">
        <v-row class="courseSearch">
          <v-autocomplete :items="courses" v-model="selectedCourse" label="Search for a course ..."
                          clearable hint="Ex. 'CSCA08H3' or 'Elementary Musicianship I'" flat color="warning">
          </v-autocomplete>
        </v-row>
        <v-row class="subCourseSearch">
          <v-text-field v-model="search" label="Filter sub directory courses ..." hint="Ex. 'CSCA08H3' or 'Elementary Musicianship I'"
            flat clearable class="courseSearch" color="purple"
          />
        </v-row>
        <!-- Button grid to hold the directory letters -->
        <v-row>
          <v-btn class="dirButtons" color="primary" x-large icon
                 v-for="dir in topDirectory1" v-bind:key="dir.letter"
                 @click="selectedSubDir(dir.letter)">{{ dir.letter }}</v-btn>
        </v-row>
        <v-row>
          <v-btn class="dirButtons" color="primary" x-large icon
                 v-for="dir in topDirectory2" v-bind:key="dir.letter"
                 @click="selectedSubDir(dir.letter)">{{ dir.letter }}</v-btn>
        </v-row>
        <!-- Tree view section with its attributes/qualities  -->
        <v-row class="dirSide">
          <div class="listScroll">
            <v-treeview
              :items=selectedItems
              return-object
              hoverable
              dense
              activatable
              open-all
              open-on-click
              transition
              color="warning"
              rounded
              :search="search"
              :open.sync="open"
            >
              <!-- This template allows for events on every course so can bring up course info when clicked -->
              <template slot="label" slot-scope="{ item }">
                <a @click="getCourseInfo(item)">{{ item.name }}</a>
              </template>
              <template v-slot:prepend="{ item }">
                <v-icon
                  v-if="item.children"
                  v-text="`mdi-${item.id === 1}`"
                />
              </template>
            </v-treeview>
          </div>
        </v-row>
      </v-col>

      <v-divider vertical/>

      <!-- Right column to hld the course information -->
      <v-col>
        <v-tabs background-color="transparent" color="primary" grow>
          <v-tab v-on:click="selectedTab('I')"><b>Course Information</b></v-tab>
          <v-tab v-on:click="selectedTab('C')"><b>Student Comments</b></v-tab>
        </v-tabs>
        <v-container v-if="this.tab==='I'" class="pt-5 pr-0">
          <!-- If they've clicked a course display the information -->
          <div class="align-center" v-if="courseInfo.name !== 'Select a course to view more information ...'">
            <h1>{{ courseInfo.name }}</h1>
            <br><br>
            <h2>Course Information:</h2>
            {{ courseInfo.desc }}
            <br><br>
            <h2>Prerequisites:</h2>
            {{ courseInfo.pre }}
            <br><br>
            <h3>Exclusions:</h3>
            {{ courseInfo.excl }}
            <br><br>
            <h3>Student Limit:</h3>
            {{ courseInfo.limit }}
            <br><br>
            <h3>Breadth Requirement:</h3>
            {{ courseInfo.breadth }}
            <br><br>
            <h3>Future Course Outlook (Courses that use this course as a prerequisite):</h3>
            {{ courseInfo.unlocked }}
          </div>
          <!-- If they haven't selected a course output a default message-->
          <div v-else class="emptyInfo">
            <h2>Oops nothing to see here <br> {{ courseInfo.name }}</h2>
            <img src="../assets/Oops.png" height="300" width="300"/>
          </div>

        </v-container>
        <v-container v-else class="pt-5 pr-0">
          <div v-if="courseInfo.name !== 'Select a course to view more information ...'">
            <h2>View & Add Course Comments - {{ courseInfo.name.substring(0,8) }}</h2>
            <v-row>
              <v-container v-if="this.$store.state.user.access >= 2" class="px-0 mx-0 py-0">
                <small class="pl-3">*Note: Any offensive comments will be removed and that user will lose the ability to create comments</small>
                <v-container class="pa-0">
                  <v-row>
                    <v-col cols="12" sm="6" md="4" class="pb-0">
                      <v-select label="Difficulty" v-model="userComment.difficulty" :items="['5', '4', '3', '2', '1']"></v-select>
                    </v-col>
                    <v-col cols="12" sm="6" md="4" class="pb-0">
                      <v-select label="Bird Course" v-model="userComment.bird" :items="['Yes', 'No']" required></v-select>
                    </v-col>
                    <v-col cols="12" sm="6" md="4" class="pb-0">
                      <v-select label="Would Recommend" v-model="userComment.recommend" :items="['Yes!', 'NO!']" required></v-select>
                    </v-col>
                    <v-col cols="12" class="py-0">
                      <v-text-field label="Comment" v-model="userComment.comment" clearable required placeholder="Leave a comment ..."></v-text-field>
                    </v-col>
                  </v-row>
                </v-container>
                <v-card-actions class="py-0">
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="submitComment()">Submit</v-btn>
                </v-card-actions>
              </v-container>
            </v-row>
            <h3 class="py-4">{{ numOfComments }} Comments</h3>
            <v-row v-if="this.numOfComments === 0" class="pt-12">
              <v-col class="pt-8">
                <h1 class="text-center">No Comments</h1>
                <h3 class="text-center">It's quiet... too quiet...</h3>
              </v-col>
            </v-row>
            <v-row class="px-0 mx-0 commentList">
              <v-row v-for="(item) in courseComments.slice().reverse()" :key="item.user" class="comment">
                <v-col class="pb-0">
                  <v-row class="pl-3">
                    <h4>{{ item.user }}</h4><h6 class="pl-3 pt-1">{{ item.date }}</h6>
                  </v-row>
                  <v-row class="commentRatings py-0">
                    <v-col class="pt-0"><h5>Would Recommend: {{ item.recommend }}</h5></v-col>
                    <v-col class="pt-0"><h5>Content Difficulty: {{ item.difficulty }}</h5></v-col>
                    <v-col class="pt-0"><h5>Bird Course: {{ item.bird }}</h5></v-col>
                  </v-row>
                  <p>{{ item.comment }}</p>
                </v-col>
              </v-row>
            </v-row>
          </div>
          <div v-else class="emptyInfo">
            <h2 class="align-center">Really? Still nothing to show<br>Select a course to view comments ...</h2>
            <img src="../assets/comment.png" height="300" width="300"/>
          </div>
        </v-container>
      </v-col>

    </v-row>

  </v-container>

</template>

<script>
// Import axios since using APIs to fetch data
import axios from 'axios'
export default {
  data: () => ({
    tab: 'I',
    numOfComments: 5,
    userComment: { user: 'RiceBoy', difficulty: 0, bird: ' N/A ', recommend: ' N/A ', comment: '', date: '', course: '', courseid: '' },
    // Course info object
    courseInfo: { id: '',
      name: 'Select a course to view more information ...',
      desc: '',
      pre: '',
      excl: '',
      limit: '',
      breadth: '',
      unlocked: '' },
    // Course comments
    // courseComments: [],
    // Treeview course data
    items: [],
    selectedItems: [],
    courses: [],
    selectedCourse: '',
    selectedCourseObject: { name: 'I like rice' },
    open: [1, 2],
    search: null,
    caseSensitive: false,
    searching: false,
    topDirectory1: [ { letter: 'A' }, { letter: 'B' }, { letter: 'C' }, { letter: 'D' }, { letter: 'E' }, { letter: 'F' }, { letter: 'G' }, { letter: 'H' }, { letter: 'I' } ],
    topDirectory2: [ { letter: 'J' }, { letter: 'L' }, { letter: 'M' }, { letter: 'N' }, { letter: 'P' }, { letter: 'R' }, { letter: 'S' }, { letter: 'T' }, { letter: 'W' } ],
    courseComments: [
      { user: 'Justin Lyn', difficulty: 5, bird: 'Yes', recommend: 'Yes!', comment: 'BLAH BLAH BLAH BLAH', date: 'January 12/2020' },
      { user: 'Bob', difficulty: 3, bird: 'Yes', recommend: 'NO!', comment: 'BLAH BLAH BLAH BLAH BLAH BLAH BLAH BLAH BLAH BLAH BLAH BLAH BLAH BLAH BLAH BLAH BLAH BLAH BLAH BLAH', date: 'February 12/2020' },
      { user: 'RiceBoy', difficulty: 4, bird: 'No', recommend: 'Yes!', comment: 'BLAH BLAH BLAH BLAH', date: 'March 12/2020' },
      { user: 'Ashley', difficulty: 1, bird: 'Yes', recommend: 'Yes', comment: 'BLAH BLAH BLAH BLAH BLAH BLAH BLAH BLAH BLAH BLAH BLAH BLAH BLAH BLAH BLAH BLAH', date: 'April 12/2020' },
      { user: 'Timothy E', difficulty: 2, bird: 'No', recommend: 'NO!', comment: 'BLAH BLAH BLAH BLAH BLAH BLAH BLAH BLAH', date: 'May 12/2020' }
    ]
  }),
  // Watcher so when they select from the autocomplete we can call the function to get the info
  watch: {
    selectedCourse: function (newCourse) {
      // Check so we don't get undefined (happens when they clear the field)
      if (typeof newCourse !== 'undefined') {
        // Set the object name and pass it in
        this.selectedCourseObject.name = newCourse
        this.getCourseInfo(this.selectedCourseObject)
      }
    }
  },
  // API call upon creation to populate the course directory
  created () {
    axios.get('http://127.0.0.1:5000/DataRetrieval/directory')
      .then(response => {
        // Run a loop to append the data
        for (let section in response.data) {
          this.items.push(response.data[section])
          // Default the selected options to show A directory
          if (response.data[section].name === 'A') {
            this.selectedItems.push.apply(this.selectedItems, response.data[section].children)
          }
        }
      })
      // Catch any errors
      .catch(e => {
        this.errors.push(e)
      })
    // API call to get just the courses with no divisions for autocomplete section
    axios.get('http://127.0.0.1:5000/DataRetrieval/courses/1')
      .then(response => {
        // Run a loop to append the data
        for (let course in response.data) {
          this.courses.push(response.data[course].name)
        }
      })
      // Catch any errors
      .catch(e => {
        this.errors.push(e)
      })
  },
  // Filter for search functionality
  filter () {
    return this.caseSensitive
      ? (item, search, textKey) => item[textKey].indexOf(search) > -1
      : undefined
  },
  methods: {
    // This method will create an API call to get the info related to the course and update the variable
    getCourseInfo: function (courses) {
      // Array to store course letters to check if they clicked on a course or no
      let alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'W']
      // If they clicked on a letter or category and not a course output a default message
      if ((alphabet.includes(courses.name)) || !(courses.name.match(/[A-Z]{4}[0-9]{2}[A-Z][0-9]/))) {
        this.courseInfo.name = 'Select a course to view more information ...'
      } else {
        // If they actually clicked a course use API call passing in course to get its info
        let url = 'http://127.0.0.1:5000/DataRetrieval/courseInfo/' + courses.name
        axios.get(url)
          .then(response => {
            let info = (response.data)
            // Fill the object with the course information to output
            this.courseInfo.id = info.id
            this.courseInfo.name = courses.name
            this.courseInfo.desc = info.desc
            this.courseInfo.pre = info.pre
            this.courseInfo.excl = info.ex
            this.courseInfo.limit = info.limit
            this.courseInfo.breadth = info.breadth
            if (info.unlocked.length === 0) {
              this.courseInfo.unlocked = 'N/A'
            } else {
              this.courseInfo.unlocked = info.unlocked
            }
            this.courseComments = info.comments
            this.numOfComments = this.courseComments.length
          })
          // Catch any errors
          .catch(e => {
            this.errors.push(e)
          })
      }
    },
    // Function which will clear and then reload the subdir based on the button they select
    selectedSubDir: function (course) {
      this.selectedItems = []
      this.searching = false
      // Loop through the course directory until we find the right sub section
      this.items.forEach((element) => {
        if (element.name === course) {
          this.selectedItems.push.apply(this.selectedItems, element.children)
        }
      })
    },
    // Function that switches the tab on selection
    selectedTab: function (tab) {
      if (tab === 'C') {
        this.tab = 'C'
      } else {
        this.tab = 'I'
      }
    },
    submitComment: function () {
      // Fill out the date stamp and course information
      this.userComment.date = new Date().toLocaleString()
      this.userComment.courseid = this.courseInfo.id
      this.userComment.course = this.courseInfo.name
      this.courseComments.push(this.userComment)
      this.numOfComments = this.courseComments.length
      // Save the comment in the database
      let comment = { comment: this.userComment }
      axios.post('http://127.0.0.1:5000/DataPosting/comment', comment)
        .then(response => {
          if (response.data === 'ERROR') {
            this.showSnack('Error submitting comment!')
          } else {
            // Show snackbar confirmation
            this.showSnack('Comment saved!')
          }
        })
        .catch(e => {
          this.showSnack('An error occurred!' + e)
        })
      // Reset
      this.userComment = { user: 'RiceBoy', difficulty: 0, bird: ' - ', recommend: ' - ', comment: '', date: '', course: '', courseid: '' }
    }
  }
}

</script>

<style scoped>
  h6{
    color: grey;
  }
  .dirSide{
    padding-top: 10px;
  }
  .listScroll{
    height: 56vh;
    min-width: 95%;
    overflow-y: auto;
  }
  .container{
    max-width: 95%;
    max-height: inherit;
  }
  .courseSearch{
    max-width: 95%;
  }
  .subCourseSearch{
    max-width: 100%;
  }
  .emptyInfo{
    text-align: center;
    height: 50%;
    padding-top: 20%;
  }
  .dirButtons{
    position: relative;
    padding-left: 5%;
    padding-right: 5%;
    font-weight: bold;
    font-size: 20px;
  }
  .commentList{
    min-width: 100%;
  }
  .comment{
    min-width: 100%;
  }

</style>
