<script setup>
const props = defineProps(['id', 'artifact'])
import OpenLimeViewer from '../components/rti/OpenLimeViewer.vue'
import ImageThumbnailList from '../components/ImageThumbnailList.vue';
import ArtifactThumbnailList from '../components/ArtifactThumbnailList.vue';
// import { getArtifact } from '../utils';
import ArtifactForm from '../components/ArtifactForm.vue'
import ArtifactDetails from '../components/ArtifactDetails.vue'

import { ref, onMounted } from 'vue'


const artifact = ref()
const selectedMedia = ref("")
const isEditing = ref(false)

async function getArtifact(id) {
  try {
    const res = await fetch(`http://localhost:8000/artifacts/${id}`)  // replace with your API URL
    if (!res.ok) throw new Error('Failed to fetch artifact')
    artifact.value = (await res.json()).artifact
    selectedMedia.value = getDefaultMedia(artifact.value)
  } catch (error) {
    console.error(error)
  }
}
// console.log('artifact:', artifact);
// console.log(artifact.relightableMedia);
onMounted(() => {
  getArtifact(props.id)
})


function getDefaultMedia(artifact) {
  if (artifact.relightableMedia.length > 0) {
    return artifact.relightableMedia[0].url
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
  const formData = new FormData()
  formData.append('metadata', JSON.strigify({
    
  }))
  formData.append('title', a.title)
  formData.append('description', a.description)
  formData.append('creator', a.creator)
  formData.append('date', a.date)
  formData.append('copyright', a.copyright)
  
  console.log(a.images)
  for (const file of a.images) {
    formData.append('images', file) // Note: repeated key name for FastAPI List[UploadFile]
  }
  
  try {
    const response = await fetch(`http://localhost:8000/artifacts/${artifact.value.id}`, {
      method: 'PUT',
      body: formData
    })
    
    if (response.ok) {  // true for 200–299 status codes
      const data = await response.json()
      console.log('Upload successful:', data)
      isEditing.value = false
      getArtifact(props.id)
    } else {
      console.log('Upload failed with status:', response.status)
      // optionally parse error JSON:
      try {
        const errorData = await response.json()
        console.log('Error details:', errorData)
      } catch {
        // no JSON body
      }
    }
  } catch (error) {
    console.error('Upload failed:', error)
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
    :rtis="artifact.relightableMedia"
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
    Relightable Images ({{ artifact.relightableMedia.length }})
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
  :media="artifact.relightableMedia"
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