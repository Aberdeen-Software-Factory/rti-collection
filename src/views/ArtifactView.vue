<script setup>
const props = defineProps(['id', 'artifact'])
import OpenLimeViewer from '../components/rti/OpenLimeViewer.vue'
import ImageThumbnailList from '../components/ImageThumbnailList.vue';
import ArtifactThumbnailList from '../components/ArtifactThumbnailList.vue';
// import { getArtifact } from '../utils';

import { ref, onMounted } from 'vue'


const artifact = ref()
const selectedMedia = ref("")

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
</script>

<template>
  <div v-if="artifact">
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
    
    <h1>{{ artifact.title }}</h1>
    <table>
      <tbody>
        <tr>
          <th>Description</th>
          <td>{{ artifact.description }}</td>
        </tr>
        <tr>
          <th>Creator</th>
          <td>{{ artifact.creator }}</td>
        </tr>
        <tr>
          <th>Date</th>
          <td>{{ artifact.date }}</td>
        </tr>
        <tr>
          <th>Copyright</th>
          <td>{{ artifact.copyright }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
table {
    width: 100%;
    border-spacing: 0 0.5rem; /* horizontal gap: 0, vertical gap: 1rem */
    border-collapse: separate;
    margin-top: 1rem;
}

th {
    text-align: left;
    vertical-align: top;
    font-weight: bold;
    white-space: nowrap; /* Prevent label wrapping */
    width: 1%; /* Shrink to fit content */
    padding-right: 1rem;
}

td {
    width: auto; /* Take remaining space */
    padding: 0;
}
</style>