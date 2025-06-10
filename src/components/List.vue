<script setup>
import ArtifactCard from './ArtifactCard.vue';
import artifactList from './data.js';
// import { getArtifacts } from '../utils';

import { ref, onMounted } from 'vue'

const artifacts = ref([])

async function getArtifacts() {
  try {
    const res = await fetch('http://localhost:8000/artifacts/')  // replace with your API URL
    if (!res.ok) throw new Error('Failed to fetch artifacts')
    artifacts.value = (await res.json()).artifacts
  } catch (error) {
    console.error(error)
  }
}

// Fetch artifacts when component mounts
onMounted(() => {
  getArtifacts()
})
</script>

<template>
    <div class="main">
        <ArtifactCard
          v-for="(artifact, index) in artifacts"
          :key="index"
          :artifact="artifact"
          @click="() => $router.push({ name: 'artifact', params: { id: artifact.id } })"
    />
    </div>
</template>

<style scoped>
.main {
  padding:10px;
  display:grid;
  grid-template-columns: 1fr;
  gap:10px;
}

@media (min-width:414px){
  .main{
    grid-template-columns: 1fr 1fr;
  }
}

@media (min-width:768px){
  .main{
    grid-template-columns: 1fr 1fr 1fr;
  }
}

@media (min-width:1200px){
  .main{
    grid-template-columns: 1fr 1fr 1fr 1fr;
  }
}
</style>