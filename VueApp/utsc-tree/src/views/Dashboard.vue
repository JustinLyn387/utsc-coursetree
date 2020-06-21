<template>
  <div class="dashPage">
    <DashboardPage></DashboardPage>
  </div>
</template>

<script>
import DashboardPage from '@/components/DashboardPage'
export default {
  name: 'Dashboard',
  components: {
    DashboardPage
  }
}
</script>

<style scoped>
  .dashPage{
    background-color: cornflowerblue;
  }

</style>
