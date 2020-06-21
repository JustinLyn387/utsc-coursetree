<template>
  <modal class="feedbackPopup" name="feedbackPopup" transition="pop-out" :width="700" :height="800">
    <v-container class="feedbackForm">
      <iframe src="https://docs.google.com/forms/d/e/1FAIpQLSdmvVczSbu1OmoM2eZO2XJCIfPyGDZKNNOwGD-L_hzZ6scpHw/viewform?embedded=true" width="700" height="800">Loading…</iframe>
    </v-container>
  </modal>
</template>

<script>

export default {
  name: 'FeedbackModal'
}
</script>

<style scoped>
  .feedbackForm {
    padding: 0;
  }
  input:focus {
    outline: none;
  }
</style>
