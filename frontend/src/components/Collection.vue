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
  <div class="max-w-340 mx-auto p-8 grid sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
    <RouterLink
      v-for="(artifact, index) in artifacts"
      :to="`/artifacts/${artifact.id}`"
    >
      <ArtifactCard :key="index" :artifact="artifact"/>
    </RouterLink>
  </div>
</template>

