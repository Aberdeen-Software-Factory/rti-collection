<script setup>
import RelightViewer from './components/RelightViewer.vue'
</script>

<template>
  <main>
    <!-- <RelightViewer url="test/bilinear18" /> -->
    <RelightViewer url="test-image" />
  </main>
</template>

<style scoped>
main {
  display: flex;
  flex-direction: column;
}
</style>
