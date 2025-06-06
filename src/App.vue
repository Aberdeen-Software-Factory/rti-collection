<script setup>
import RelightViewer from './components/RelightViewer.vue'
import List from './components/List.vue'
</script>

<template>
  <main>
    <List/>
    <!-- <RelightViewer url="test/bilinear18" /> -->
    <!-- <RelightViewer url="test-image" /> -->
  </main>
</template>

<style scoped>
main {
  display: flex;
  flex-direction: column;
}
</style>
