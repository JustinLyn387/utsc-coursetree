<template>
  <modal class="textSamplePopup" name="textSamplePopup" transition="pop-out" :width="700" :height="350">
    <v-container class="samplePopupContainer">
      <v-img class="image" src="../assets/SampleTranscript.png"></v-img>
    </v-container>
  </modal>
</template>

<script>
export default {
  name: 'TextSampleModal'
}
</script>

<style scoped>
  .samplePopupContainer{
    padding: 0;
    min-height: 100%;
    min-width: 100%;
  }
</style>
