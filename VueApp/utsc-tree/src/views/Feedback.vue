<template>
  <div class="timelineSection">
    <NewsFeedbackPage></NewsFeedbackPage>
  </div>

</template>

<script>
import NewsFeedbackPage from '@/components/NewsFeedbackPage'
export default {
  name: 'News',
  components: {
    NewsFeedbackPage
  }
}
</script>

<style scoped>
  .timelineSection{
    background-color: #E3F2FD;
  }

</style>
