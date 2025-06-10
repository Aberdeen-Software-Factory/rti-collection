<script setup>
import RelightViewer from './components/rti/RelightViewer.vue'
import OpenLimeViewer from './components/rti/OpenLimeViewer.vue'
import List from './components/List.vue'

import artifactList from './components/data.js'

</script>

<template>
  <main>
    <!-- <List/> -->
    <!-- <RelightViewer url="test/bilinear18" /> -->
    <!-- <RelightViewer url="test-image" /> -->
     <!-- <OpenLimeViewer url="test-image"/> -->
      <p>
    <strong>Current route path:</strong> {{ $route.fullPath }}
  </p>
  <RouterLink to="/">Collection</RouterLink>
  <RouterLink to="/artifact/artifact-001">Go to About</RouterLink>
  <RouterLink to="/upload">Upload</RouterLink>
  <RouterView/>
    <!-- <ArtifactDetail v-bind:artifact="artifactList[0]"/> -->
     <!-- <OpenLimeThumbnail url="test/ptm"/>
     <OpenLimeThumbnail url="test-image"/> -->
  </main>
</template>

<style scoped>
main {
  display: flex;
  flex-direction: column;
}
</style>
