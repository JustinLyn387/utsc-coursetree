<template>
  <v-container class="aboutContainer">
    <v-row class="mainRows">
      <v-card class="aboutCards" shaped>
        <v-row class="rowSection">
          <v-col class="colSection">
            <h1>- Our Goal -</h1>
            <p>To provide the best platform and user experience for students to plan and pick their courses.</p>
          </v-col>
        </v-row>
        <v-row class="rowSection">
          <v-col class="colSection">
            <h1>- About -</h1>
            <p>UTSC CourseTree was created by students for students without all the tabs! For all current and future students we are sure you know what we
              are talking about. With this website we hope to simplify and improve students' experience when picking courses and checking prerequisites
              by implementing courses in a tree like structure to show you all the information you need in one place! This site took a little over 6 months
              to create and we are committed to providing users with the best platform to use, so if you have any feedback or requests let us know.
              <br><br><b>We hope you enjoy this website as much as we do!</b></p>
          </v-col>
        </v-row>
      </v-card>
    </v-row>

    <v-row class="mainRows">
      <v-card class="aboutCards" shaped>
        <v-row class="rowSection">
          <v-col class="colSection">
            <h1>- The Team -</h1>
            <v-row class="profileRow">
              <v-col class="teamCols">
                <img src="../assets/uoft-logo.png" height="200" width="200"/>
                <h2>Justin Lyn</h2>
                <p>Co-Founder & Full Stack Developer</p>
              </v-col>
              <v-col class="teamCols">
                <img src="../assets/uoft-logo.png" height="200" width="200"/>
                <h2>Rahul Ramani</h2>
                <p>Co-Founder & Back-End Engineer</p>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-card>
    </v-row>

    <v-row class="mainRows">
      <v-card class="aboutCards" shaped>
        <v-row class="rowSection">
          <v-col class="colSection">
            <h1>- Contact Us -</h1>
            <p>If you have issues, feedback, or feature requests please fill out the Feedback form on the <b>News & Feedback</b> page.
              <br><br>For any other inquiries or questions feel free to send us an email at: <b>utsc.courstree@outlook.com</b></p>
          </v-col>
        </v-row>
      </v-card>
    </v-row>

  </v-container>

</template>

<script>
export default {
  name: 'AbtCredPage'
}
</script>

<style scoped>
  @import url('https://fonts.googleapis.com/css?family=Montserrat&display=swap');
  h1{
    padding-bottom: 20px;
  }
  p{
    text-align: center;
  }
  .aboutContainer{
    width: 90%;
    padding-top: 30px;
    background-color: #E3F2FD;
  }
  .rowSection{
    width: 100%;
    padding-bottom: 20px;
    margin: 0;
    font-family: 'Montserrat';
    justify-content: center;
  }
  .colSection{
    text-align: center;
    justify-content: center;
    max-width: 80%;
  }
  .teamCols{
    width: 50%;
    padding-left: 5px;
    padding-right: 5px;
  }
  .profileRow{
    padding-left: 7%;
    padding-right: 7%;
  }
  .aboutCards{
    padding-top: 10px;
    width: 82%;
  }
  .mainRows{
    padding-bottom: 15px;
    justify-content: center;
  }

</style>
