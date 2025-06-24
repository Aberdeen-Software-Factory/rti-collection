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
  <div v-if="artifacts.length > 0" class="max-w-340 mx-auto p-4 md:p-8 grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
    <RouterLink
      v-for="(artifact, index) in artifacts"
      :to="`/artifacts/${artifact.id}`"
    >
      <ArtifactCard :key="index" :artifact="artifact"/>
    </RouterLink>
  </div>

  <div v-else class="hero bg-base-200 flex-grow">
      <div class="hero-content text-center">
        <div class="max-w-md">
          <h1 className="text-5xl font-bold">Empty collection</h1>
          <p className="py-6">
            There are no artifacts in this collection. Start by uploading some if you are authorised.
          </p>
          <RouterLink to="/upload" className="btn btn-primary">Upload Artifact</RouterLink>
        </div>
      </div>
    </div>
</template>

