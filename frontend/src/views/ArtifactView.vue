<script setup>
import OpenLimeViewer from '../components/rti/OpenLimeViewer.vue'
import ArtifactThumbnailList from '../components/ArtifactThumbnailList.vue';
import MetadataDisplay from '../components/display/MetadataDisplay.vue';
import { Artifact } from '@/model/artifact';
import Header from '@/components/Header.vue';

import { ref, watch } from 'vue';
import { deleteArtifact } from '../backend.js';
import { useRouter } from 'vue-router'
import { useArtifact } from '@/composables/useArtifact';

const props = defineProps({
  id: String,
  artifact: Artifact,
})

const router = useRouter()

const { artifact, error } = useArtifact(props.id)
const selectedMedia = ref("")

watch(artifact, (newArtifact) => {
  if (newArtifact?.RTIs?.length > 0) {
    selectedMedia.value = getDefaultMedia(newArtifact);
  }
})

function getDefaultMedia(artifact) {
  if (artifact.RTIs.length > 0) {
    return artifact.RTIs[0].url
  } else if (artifact.images.length > 0) {
    return artifact.images[0]
  } else {
    return ""
  }
}

async function onDeleteClicked() {
  if (confirm("Are you sure you want to delete this artifact? This action cannot be undone.")) {
    try {
      await deleteArtifact(artifact.value.id);
      router.replace('/');
    } catch {
      alert("Unable to delete artifact.");
    }
  }
}

</script>

<template>
  <Header :segments="[
    { label: 'Collection', dest: '/' },
    { label: artifact?.metadata.name || 'Artifact' }
  ]" :title="artifact?.metadata.name || 'Artifact'" />

  <div v-if="artifact">
    <OpenLimeViewer :url="selectedMedia" />
    <!-- <NewViewer :url="selectedMedia"/> -->
    <div class="bg-base-300">
      <div class="max-w-340 mx-auto">
        <div v-if="artifact.RTIs.length > 0" class="md:px-8 pt-4">
          <p class="py-2">Relightable Images ({{ artifact.RTIs.length }}):</p>
          <ArtifactThumbnailList v-model="selectedMedia" :options="artifact.RTIs.map((rti) => ({
            thumbnail: rti.files.find(f => f.endsWith('plane_0.jpg')) || '',
            value: rti.url
          }))" />
        </div>

        <div v-if="artifact.images.length > 0" class="md:px-8 pt-4">
          <p class="py-2">Still Images ({{ artifact.RTIs.length }}):</p>
          <ArtifactThumbnailList v-model="selectedMedia" :options="artifact.images.map((imageUrl) => ({
            thumbnail: imageUrl,
            value: imageUrl
          }))" />
        </div>

        <div class="md:px-8 pt-4">
          <h2 class="text-3xl">Details:</h2>
          <MetadataDisplay :metadata="artifact.metadata" />
        </div>
      </div>
      <div class="bg-base-200 border-base-300 border-t">
        <div class="max-w-340 mx-auto md:px-8 py-8 flex gap-2 justify-end">
          <!-- <h1 style="flex-grow: 1;">{{ artifact.metadata.name || "Artifact" }}</h1> -->
          <RouterLink :to="`/artifacts/${id}/edit`" class="btn">Edit</RouterLink>
          <button @click="onDeleteClicked" class="btn">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
a {
  width: fit-content;
  color: inherit;
}

a:hover {
  text-decoration: none;
}
</style>