<script setup>
import ArtifactCard from './ArtifactCard.vue';
import { fetchArtifacts } from '../backend'
import { ref, onMounted } from 'vue'

const artifacts = ref([])

onMounted(async () => {
  artifacts.value = await fetchArtifacts();
})
</script>

<template>
  <div class="main">
    <RouterLink v-for="(artifact, index) in artifacts" :to="`/artifacts/${artifact.id}`">
      <ArtifactCard :key="index" :artifact="artifact"/>
    </RouterLink>
  </div>
</template>

<style scoped>
.main {
  padding: 30px 0;
  display:grid;
  grid-template-columns: 1fr;
  gap:40px;
}

a {
  text-decoration: none;
  color: inherit;
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