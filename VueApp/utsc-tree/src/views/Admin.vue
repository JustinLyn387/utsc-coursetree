<template>
  <div class="adminPage">
    <AdminPage></AdminPage>
  </div>

</template>

<script>
import AdminPage from '@/components/AdminPage.vue'
export default {
  name: 'Admin',
  components: {
    AdminPage
  }
}
</script>

<style scoped>
  h1{
    padding-top: 15px;
    padding-left: 20px;
    text-align: center;
  }
  .adminPage{
    background-color: #3b5998;
  }

</style>
