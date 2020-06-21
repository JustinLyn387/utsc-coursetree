<template>
  <div class="aboutsPage">
    <AbtCredPage></AbtCredPage>
  </div>

</template>

<script>
import AbtCredPage from '@/components/AboutAndCredits.vue'
export default {
  name: 'Credits',
  components: {
    AbtCredPage
  }

}
</script>

<style scoped>
  .aboutsPage{
    background-color: #E3F2FD;
  }

</style>
