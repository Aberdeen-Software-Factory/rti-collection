<script setup>
const props = defineProps({
  id: String,
  artifact: Artifact,
})

import OpenLimeViewer from '../components/rti/OpenLimeViewer.vue'
import ImageThumbnailList from '../components/ImageThumbnailList.vue';
import ArtifactThumbnailList from '../components/ArtifactThumbnailList.vue';
import ArtifactEditor from '../components/ArtifactEditor.vue'
import MetadataDisplay from '../components/display/MetadataDisplay.vue';

import { ref, onMounted } from 'vue';
import { fetchArtifact, updateArtifact, deleteArtifact } from '../backend.js';
import { useRouter } from 'vue-router'
import { Artifact } from '@/model/artifact';

const router = useRouter()

const artifact = ref()
const selectedMedia = ref("")
const isEditing = ref(false)

const imageFiles = ref([])
const RTIFiles = ref([])

onMounted(async () => {
  artifact.value = await fetchArtifact(props.id);
  selectedMedia.value = getDefaultMedia(artifact.value);

  console.log(artifact.value)
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

async function onEditClicked() {
  isEditing.value = !isEditing.value
}

async function onDeleteClicked() {
  if (confirm("Are you sure you want to delete this artifact? This action cannot be undone.")) {
    try {
      await deleteArtifact(artifact.value.id);
      router.push('/');
    } catch {
      alert("Unable to delete artifact.");
    }
  }
}

async function handleSubmit(a) {
  console.log("form", a)
  console.log(artifact)
  
  // event.preventDefault();
  
  try {
    console.log(a)
    const res = await updateArtifact(a.id, {
      metadata: a.metadata,
      images: a.imageFiles,
      webrtis: a.webrtiFiles,
      ptms: a.ptmFiles,
    });
    console.log(res);
    isEditing.value = false
    
    artifact.value = await fetchArtifact(props.id);
    selectedMedia.value = getDefaultMedia(artifact.value);
  } catch (error) {
    console.log(error)
  }
}
</script>

<template>
  <RouterLink to="/">Back to Collection</RouterLink>
  <section v-if="isEditing">
    <h1>Edit Artifact</h1>
    <ArtifactEditor v-if="artifact"
    :artifact="artifact"
    @submit="handleSubmit"
    >
    <button @click="isEditing = false">Cancel</button>
    <button type="submit">Save</button>
  </ArtifactEditor>
</section>
<div v-if="artifact && !isEditing">
  <div style="display: flex;">
    <h1 style="flex-grow: 1;">{{ artifact.metadata.name || "Artifact" }}</h1>
    <button @click="onEditClicked" class="link-style">Edit</button>
    <button @click="onDeleteClicked" class="link-style">Delete</button>
  </div>
  
  <OpenLimeViewer :url="selectedMedia"/> 
  <!-- <NewViewer :url="selectedMedia"/> -->
  
  <p v-if="artifact.RTIs.length > 0">
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
  v-if="artifact.images.length > 0"
  v-model:selectedUrl="selectedMedia"
  :urls="artifact.images"
  />
  
  <MetadataDisplay :metadata="artifact.metadata"/>
  
  <br/>
  
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