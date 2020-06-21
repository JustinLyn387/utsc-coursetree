<template>
  <v-container class="mainContainer">
    <FeedbackModal/>
    <v-row class="mainRow">
      <v-col class="mainCol">
        <v-card shaped class="feedbackCard">
          <v-row>
            <v-col class="innerColumn">
              <v-container class="pa-0">
                <v-col>
                  <v-row class="innerRow">
                    <h2>- Leave Feedback -</h2>
                    <p class="feedbackSection">Let us know how your experience was, we'd love to know!
                      If you have any feedback or feature requests, let us know by clicking the button below and filling out the form!
                      <br><br>Don't have time? Leave a quick rating for now
                    </p>
                  </v-row>
                  <v-row class="innerRow">
                    <v-rating class="ratingStars" v-model="rating" color="yellow darken-3" background-color="grey darken-1" empty-icon="$ratingFull"
                              half-increments hover medium>
                    </v-rating>
                  </v-row>
                  <v-row class="text-md-center pt-0">
                    <v-flex>
                      <!--- v-flex is centered now, but we need to center button inside v-flex -->
                      <div class="text-xs-center">
                        <v-btn class="mr-3 feedbackButton" color="green accent-3" v-on:click="$modal.show('feedbackPopup')">Feedback Form</v-btn>
                        <v-btn class="ml-3" color="primary">Submit Rating</v-btn>
                      </div>
                    </v-flex>
                  </v-row>
                </v-col>

              </v-container>
            </v-col>
            <v-divider vertical/>
            <v-col class="innerColumn">
              <v-container class="pa-0">
                <v-col>
                  <v-row class="innerRow pb-2">
                    <h2>- Developer Messages -</h2>
                  </v-row>
                  <v-row class="newsFeed">
                    <!-- Loop through the array to populate the feed and create the list items -->
                    <v-list two-line class="feedList">
                      <v-list-item-group>
                        <template v-for="(item, index) in devMessages.slice().reverse()">
                          <v-list-item :key="item.messageTitle">
                            <v-list-item-content>
                              <h4 v-text="item.messageTitle"></h4>
                              <p class="text--primary" v-text="item.messageBody"></p>
                              <v-list-item-subtitle class="float-right" v-text="item.date"></v-list-item-subtitle>
                            </v-list-item-content>
                          </v-list-item>
                          <v-divider v-if="index + 1 < devMessages.length" :key="index"></v-divider>
                        </template>
                      </v-list-item-group>
                    </v-list>
                  </v-row>
                </v-col>
              </v-container>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
    <v-row class="mainRow">
      <v-col class="mainCol">
        <v-card shaped class="px-8">
          <h2 class="sectionHeaders">- Updates & Releases -</h2>
          <v-timeline>
            <!-- Use a loop to create the timeline -->
            <v-timeline-item v-for="(item, i) in releaseNotes.slice().reverse()" :key="i" :color="item.Colour" small>
              <template v-slot:opposite>
                <span :class="`headline font-weight-light ${item.Colour}--text`" v-text="item.noteDate"></span>
              </template>
              <div class="py-4">
                <h2 :class="`headline font-weight-bold mb-4 ${item.Colour}--text`">{{ item.noteTitle }}</h2>
                <div>
                  {{ item.noteBody }}
                </div>
              </div>
            </v-timeline-item>
          </v-timeline>
        </v-card>
      </v-col>
    </v-row>

  </v-container>

</template>

<script>
import FeedbackModal from './FeedbackModal'

export default {
  name: 'NewsFeedbackPage',
  components: {
    FeedbackModal
  },
  data: () => ({
    side: true,
    rating: 4.5,
    releaseNotes: [],
    devMessages: []
  }),
  filters: {
    reverse: function (arr) {
      return arr.reverse()
    }
  },
  created () {
    this.devMessages = this.$store.state.devMessages
    this.releaseNotes = this.$store.state.releaseNotes
  }
}
</script>

<style scoped>
  @import url('https://fonts.googleapis.com/css?family=Montserrat&display=swap');
  h3{
    color:white;
  }
  h2{
    font-family: 'Montserrat';
  }
  .sectionHeaders {
    padding-top: 20px;
    padding-bottom: 10px;
    text-align: center;
  }
  .mainContainer{
    max-width: 90%;
    padding-top: 25px;
    background-color: #E3F2FD;
    min-height: 95vh;
  }
  .mainRow{
    justify-content: center;
    padding-bottom: 20px;
  }
  .innerRow{
    justify-content: center;
    padding-left: 20px;
    padding-right: 20px;
  }
  .mainCol{
    max-width: 80%;
  }
  .innerColumn{
    width: 50%;
    padding-left: 20px;
    padding-right: 20px;
    padding-bottom: 5px;
  }
  .newsFeed{
    max-height: 400px;
    padding-left: 10px;
    padding-right: 10px;
    overflow-y: auto;
  }
  .feedList{
    width: 100%;
  }
  .feedbackSection{
    text-align: center;
    font-size: 14pt;
    padding: 50px 20px 5px;
  }
  .feedbackCard{
    padding-left: 10px;
    padding-right: 10px;
  }
  .ratingStars{
    padding-bottom: 40px;
  }
  .float-right{
    text-align: right;
  }

</style>
