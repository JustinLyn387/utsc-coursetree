<template>
  <v-container>
    <gmap-map
      :center="center"
      :zoom="14"
      style="width:100%;  height: 400px;"
    >
      <gmap-marker
        :key="index"
        v-for="(m, index) in markers"
        :position="m.position"
        @click="center=m.position"
      />
    </gmap-map>
  </v-container>
</template>

<script>

export default {
  name: 'GoogleMaps',
  data () {
    return {
      // default to Montreal to keep it simple
      // change this to whatever makes sense
      center: { lat: 43.784796, lng: -79.186773 },
      markers: [{ position: { lat: 43.784796, lng: -79.186773 } }],
      places: [],
      currentPlace: null
    }
  }

}
</script>

<style scoped>

</style>
