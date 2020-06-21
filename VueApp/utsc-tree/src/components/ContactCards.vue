<template>
  <!-- Container to hold the contact cards -->
  <v-container fluid>
    <v-row dense>
      <!-- Use a for loop to populate the cards in a grid system -->
      <v-col v-for="card in cards"
             :key="card.title"
             :cols="card.flex"
      >
        <!-- Card template where we can set all the information that we want to display --->
        <v-card>
          <v-card-title v-text="card.title" class="display-1 text--primary"/>
          <v-card-subtitle v-text="card.subtitle"/>
          <v-card-text v-text="card.info" class="text--primary" id="lineBreak"/>
          <v-card-actions>
            <v-btn text color="deep-purple accent -4" :href="card.link" target="_blank">
              {{card.website}}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>

</template>

<script>
export default {
  name: 'ContactCards',
  data: () => ({
    cards: [
      { title: 'Registrars Office',
        subtitle: 'For registration, financial needs, exams, graduation, petitions, TCards, and more.',
        info: 'Location: Highland Hall (Main Floor)\nHours:\tMonday & Tuesday: 9:30-4:30\n\t\tWednesday: 10:00-4:00 & 5:00-6:45\n\t\tThursday: 9:30-4:30\n\t\tFriday: 9:30-3:00\n\nTelephone: (416) 287-7001\nEmail: Done through registrar website',
        website: 'Visit Website',
        link: 'https://www.utsc.utoronto.ca/registrar',
        flex: 6 },
      { title: 'Admissions',
        subtitle: 'For information on programs, applications, housing, finances, and campus tours.',
        info: 'Location: Highland Hall (Main Floor)\nHours:\tMonday & Tuesday: 9:30-4:30\n\t\tWednesday: 10:00-4:00 & 5:00-6:45\n\t\tThursday: 9:30-4:30\n\t\tFriday: 9:30-3:00\n\nTelephone: (416) 287-7529\nEmail: utsc.admissions@utoronto.ca',
        website: 'Visit Website',
        link: 'https://www.utsc.utoronto.ca/admissions',
        flex: 6 }
    ]
  })
}
</script>

<style scoped>
  /* Need this so it creates the new lines and tabs in strings */
  #lineBreak{
    white-space: pre-wrap;
  }

</style>
