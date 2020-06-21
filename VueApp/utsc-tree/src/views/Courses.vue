<template>
  <div>
    <h1>Course Directory</h1>
    <CourseDirectory> </CourseDirectory>
  </div>
</template>

<script>
// @ is an alias to /src
import CourseDirectory from '@/components/CourseDirectory.vue'

export default {
  name: 'courses',
  components: {
    CourseDirectory

  }
}
</script>

<style scoped>
  /*
  h1{
    padding-left: 50%;
    padding-top: 15px;
    margin-left: -125px;
  }
   */
  h1{
    padding-top: 15px;
    padding-left: 20px;
  }

</style>
