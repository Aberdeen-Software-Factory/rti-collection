<script setup>
import RelightViewer from './components/rti/RelightViewer.vue'
import OpenLimeViewer from './components/rti/OpenLimeViewer.vue'
import ArtifactDetail from './components/ArtifactDetails.vue'
import List from './components/List.vue'

import artifactList from './components/data.js'

</script>

<template>
  <main>
    <!-- <List/> -->
    <!-- <RelightViewer url="test/bilinear18" /> -->
    <!-- <RelightViewer url="test-image" /> -->
     <!-- <OpenLimeViewer url="test-image"/> -->
    <ArtifactDetail v-bind:artifact="artifactList[0]"/>
  </main>
</template>

<style scoped>
main {
  display: flex;
  flex-direction: column;
}
</style>
