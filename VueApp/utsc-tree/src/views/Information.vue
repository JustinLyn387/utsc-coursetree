<template>
  <v-container class="infoPage">
    <h1>Quick Links & Information</h1>
    <InfoPage/>
  </v-container>

</template>

<script>
import InfoPage from '@/components/InfoPage.vue'

export default {
  name: 'Information',
  components: {
    InfoPage
  }
}
</script>

<style scoped>
  h1{
    text-align: center;
  }
  .infoPage{
    max-width: 96%;
  }

</style>
