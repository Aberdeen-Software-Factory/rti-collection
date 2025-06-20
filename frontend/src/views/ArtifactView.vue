<script setup>
const props = defineProps(['id', 'artifact'])

import OpenLimeViewer from '../components/rti/OpenLimeViewer.vue'
import ImageThumbnailList from '../components/ImageThumbnailList.vue';
import ArtifactThumbnailList from '../components/ArtifactThumbnailList.vue';
import ArtifactForm from '../components/ArtifactForm.vue'
import ArtifactDetails from '../components/ArtifactDetails.vue'
import RTIThumbnail from '../components/RTIThumbnail.vue';

import { ref, onMounted } from 'vue';
import { fetchArtifact, updateArtifact, deleteArtifact } from '../backend.js';
import { fetchFiles } from '../utils.js';
import { useRouter } from 'vue-router'
import JSZip from "jszip";

const router = useRouter()

const artifact = ref()
const selectedMedia = ref("")
const isEditing = ref(false)

const imageFiles = ref([])
const RTIFiles = ref([])

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

async function onEditClicked() {
  // Download RTI files
  const zippedWebrtis = [];
  
  for (const rti of artifact.value.RTIs) {
    console.log("webrti", rti)
    const files = await fetchFiles(rti.files)
    const zip = new JSZip();
    for (const file of files) {
      zip.file(file.name, file); // Add each file to the ZIP
    }

    const zipBlob = await zip.generateAsync({ type: "blob" }); // or "base64", "uint8array", etc.

    const zipFile = new File([zipBlob], "archive.zip", { type: zipBlob.type })
    zippedWebrtis.push(zipFile);
  }
  
  RTIFiles.value = zippedWebrtis;
  
  // Download image files
  const images = await fetchFiles(artifact.value.images);
  
  imageFiles.value = images;
  
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
      metadata: {
        title: a.title,
        description: a.description,
        creator: a.creator,
        date: a.date,
        copyright: a.copyright,
      },
      images: a.images,
      webrtis: a.webrtis,
      ptms: a.ptms,
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
    <ArtifactForm v-if="artifact"
    :defaultValues="{
      id: artifact.id,
      title: artifact.title,
      description: artifact.description,
      creator: artifact.creator,
      date: artifact.date,
      copyright: artifact.copyright,
      
      images: imageFiles,
      RTIs: RTIFiles,
    }"
    @submit="handleSubmit"
    >
    <button @click="isEditing = false">Cancel</button>
    <button type="submit">Save</button>
  </ArtifactForm>
</section>
<div v-if="artifact && !isEditing">
  <h1>{{ artifact.title }}</h1>
  
  <OpenLimeViewer :url="selectedMedia"/> 
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
  <button @click="onEditClicked">Edit</button>
  <button @click="onDeleteClicked">Delete</button>
</div>
</template>

<style scoped>
a {
  color: inherit;
}

a:hover {
  text-decoration: none;
}
</style>