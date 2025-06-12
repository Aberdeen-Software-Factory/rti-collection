<script setup>
const props = defineProps(['id', 'artifact'])

import OpenLimeViewer from '../components/rti/OpenLimeViewer.vue'
import ImageThumbnailList from '../components/ImageThumbnailList.vue';
import ArtifactThumbnailList from '../components/ArtifactThumbnailList.vue';
import ArtifactForm from '../components/ArtifactForm.vue'
import ArtifactDetails from '../components/ArtifactDetails.vue'
import RTIThumbnail from '../components/RTIThumbnail.vue';

import { ref, onMounted } from 'vue';
import { fetchArtifact, updateArtifact } from '../backend.js';

const artifact = ref()
const selectedMedia = ref("")
const isEditing = ref(false)

onMounted(async () => {
  artifact.value = await fetchArtifact(props.id);
  selectedMedia.value = getDefaultMedia(artifact.value);
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

// const selectedMedia = ref('webrti')
function getThumbnailUrl(path) {
  return new URL(path, "http://localhost:8000/files").toString(); //TODO add the prefix to the openlimeviewer component
}

async function handleSubmit(event, a) {
  console.log(a)
  console.log(artifact)
  
  event.preventDefault();
  
  try {
    console.log(a)
    updateArtifact(a.id, {
      metadata: {
        title: a.title,
        description: a.description,
        creator: a.creator,
        date: a.date,
        copyright: a.copyright,
      },
    });
    console.log('Upload successful:')
    isEditing.value = false
  } catch (error) {
    console.log(error)
  }
}
</script>

<template>
  <section v-if="isEditing">
    <ArtifactForm v-if="artifact"
    :id="artifact.id"
    :title="artifact.title"
    :description="artifact.description"
    :creator="artifact.creator"
    :date="artifact.date"
    :copyright="artifact.copyright"
    :rtis="artifact.RTIs"
    :images="artifact.images"
    @submit="handleSubmit"
    >
    <button @click="isEditing = false">Cancel</button>
    <button type="submit">Save</button>
  </ArtifactForm>
</section>
<div v-if="artifact && !isEditing">
  <h1>{{ artifact.title }}</h1>
  
  <OpenLimeViewer :url="getThumbnailUrl(selectedMedia)"/> 
  <!-- <NewViewer :url="selectedMedia"/> -->
  
  <p>
    Relightable Images ({{ artifact.RTIs.length }})
    <!-- <a href="javascript:void(0) " onclick="document.getElementById('fileUpload').click()">Upload</a>
    <input 
    type="file" 
    id="fileUpload" 
    style="display: none;" 
    accept="image/*" 
    @change="handleFileUpload"
    /> -->
  </p>
  <ArtifactThumbnailList
  v-model:selected="selectedMedia"
  :media="artifact.RTIs"
  />
  
  <ImageThumbnailList
  v-model:selectedUrl="selectedMedia"
  :urls="artifact.images"
  />
  
  
  <ArtifactDetails
  :title="artifact.title"
  :description="artifact.description"
  :creator="artifact.creator"
  :date="artifact.date"
  :copyright="artifact.copyright"
  />
  <br/>
  <button @click="isEditing = !isEditing">Edit</button>
</div>
</template>

<style scoped>

</style>