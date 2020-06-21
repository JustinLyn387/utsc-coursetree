<template>
  <v-container fluid class="infoContainer">
    <v-row>
      <v-col class="leftColumn">
        <!-- This row will house the contact info cards-->

        <!-- This row will contain all the quick links -->
        <v-row>
          <v-container class="quickCard">
            <v-card class="card">
              <h2 class="linkHeader"> -  Quick Links  -</h2>
              <h3 class="linkSubHeader">Courses</h3>
              <ul>
                <li><a href="https://www.acorn.utoronto.ca" target="_blank">ACORN</a></li>
                <li><a href="https://www.utsc.utoronto.ca/home/" target="_blank">UTSC Home</a></li>
                <li><a href="https://utsc.calendar.utoronto.ca" target="_blank">UTSC Calendar</a></li>
              </ul>
              <h3 class="linkSubHeader">Schedules</h3>
              <ul>
                <li><a href="https://www.utsc.utoronto.ca/registrar/examination-schedule" target="_blank">Exam Schedules</a></li>
                <li><a href="https://www.utsc.utoronto.ca/regoffice/timetable/timetable.php" target="_blank">Course Timetable</a></li>
                <li><a href="https://www.utsc.utoronto.ca/registrar/dates-and-deadlines" target="_blank">Dates & Deadlines</a></li>
              </ul>
              <h3 class="linkSubHeader">Academics</h3>
              <ul>
                <li><a href="https://idpz.utorauth.utoronto.ca/idp/profile/SAML2/Redirect/SSO;jsessionid=EDDE3B46C59D5DF90611387C8058AEA6?execution=e1s1" target="_blank">Quercus</a></li>
                <li><a href="https://idpz.utorauth.utoronto.ca/idp/profile/SAML2/Redirect/SSO?execution=e2s1" target="_blank">WebOption</a></li>
                <li><a href="https://utsc-utoronto-csm.symplicity.com/students/?signin_tab=0&signin_tab=0" target="_blank">CSM</a></li>
              </ul>
              <h3 class="linkSubHeader">Services</h3>
              <ul>
                <li><a href="https://intranet.utsc.utoronto.ca/home.php?login=1" target="_blank">Intranet</a></li>
                <li><a href="https://weblogin.utoronto.ca/index.cgi" target="_blank">WebMail</a></li>
                <li><a href="https://www.utsc.utoronto.ca/regoffice/eservice/student/index.php" target="_blank">eService</a></li>
              </ul>
            </v-card>
          </v-container>
        </v-row>
      </v-col>

      <v-divider vertical/>
      <!-- Right column will hold quick info about UTSC -->
      <v-col class="rightColumn">
        <v-row>
          <v-col>
            <h3>UTSC Quick Info</h3>
            <GoogleMaps/>
          </v-col>
          <v-col class="rightInfoCol">
            <!-- Text and link info -->
            <h3 class="pt-4">Address & Contact Information</h3>
            <div class="utscInfo">
              <p><b>Address: </b>1265 Military Trail, Scarborough, ON M1C 1A4 <br>
                <b>Phone: </b>(416) 287-8872 <br>
                <b>Campus Police (EMERGENCY!): </b>(416) 978-2222 <br>
                <b>Campus Police (General): </b>(416) 287-7398</p>
            </div>
            <h3>Campus Map & Parking Info</h3>
            <v-row class="utscList"><a href="https://www.utsc.utoronto.ca/home/sites/utsc.utoronto.ca.home/files/docs/UTSC_Campus_Map_2015.pdf" target="_blank">Campus Map</a></v-row>
            <v-row class="utscList"><a href="https://www.utsc.utoronto.ca/parking/dailyvisitor-parking-rates" target="_blank">Parking Information</a></v-row>
            <h3 class="mediaSection">Social Media</h3>
            <a class="twitterIcon" href='https://twitter.com/UTSC?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor' target="_blank"> <font-awesome-icon :icon="['fab', 'twitter']" size="2x"/></a>
            <a class="facebookIcon" href='https://www.facebook.com/UofTScarborough/' target="_blank"><font-awesome-icon :icon="['fab', 'facebook-square']" size="2x"/></a>
            <a class="instagramIcon" href='https://www.instagram.com/utsc/' target="_blank"><font-awesome-icon :icon="['fab', 'instagram']" size="2x"/></a>
            <a class="linkedinIcon" href='https://www.linkedin.com/school/university-of-toronto/' target="_blank"> <font-awesome-icon :icon="['fab', 'linkedin-in']" size="2x"/></a>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <h3>Contacts</h3>
            <v-container class="contactCard">
              <ContactCards/>
            </v-container>
          </v-col>
        </v-row>

      </v-col>
    </v-row>

  </v-container>
</template>

<script>
import ContactCards from './ContactCards'
import GoogleMaps from './GoogleMaps'
export default {
  name: 'InfoPage',
  components: {
    GoogleMaps,
    ContactCards
  }
}

</script>

<style scoped>
  ul{
    padding-left: 0;
    padding-bottom: 25px;
  }
  li{
    padding-top: 15px;
    font-size: 12pt;
    list-style: none;
    font-weight: bold;
    text-align: center;
  }
  a:hover {
  color: skyblue;
  }
  a:link{
    text-decoration: none;
  }
  .infoContainer{
    padding: 0;
  }
  .linkHeader{
    text-align: center;
    padding-bottom: 20px;
    padding-top: 20px;
  }
  .linkSubHeader{
    text-align: center;
    font-weight: bold;
  }
  .rightColumn{
    max-width: 77%;
    padding-left: 35px;
  }
  .rightInfoCol{
    padding-top: 70px;
    padding-left: 25px;
  }
  .leftColumn{
    max-width: 23%;
    padding-right: 45px;
  }
  .card{
    background-color: white;
    padding-bottom: 10px;
  }
  .contactCard{
    padding-right: 5%;
    padding-top: 0;
    padding-left: 0;
  }
  .utscInfo{
    padding-top: 10px;
    padding-left: 20px;
  }
  .utscList{
    padding-left: 32px;
    padding-top: 10px;
    font-weight: bold;
    font-size: 13pt;
  }
  .mediaSection{
    padding-top: 15px;
  }
  .instagramIcon{
    padding-top: 5px;
  }
  .instagramIcon :hover{
    color: skyblue;
    padding-top: 7px;
  }
  .twitterIcon{
    padding-left: 20px;
    padding-right: 15px;
    color: #55acee;
  }
  .facebookIcon{
    padding-right: 15px;
    color: #3b5998;
  }
  .linkedinIcon{
    padding-left: 15px;
    color: #0976b4;
  }

</style>
