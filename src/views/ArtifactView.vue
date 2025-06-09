<script setup>
const props = defineProps(['id', 'artifact'])
import OpenLimeViewer from '../components/rti/OpenLimeViewer.vue'
import ImageThumbnailList from '../components/ImageThumbnailList.vue';
import ArtifactThumbnailList from '../components/ArtifactThumbnailList.vue';
import { getArtifact } from '../utils';

import { ref } from 'vue'


let artifact = getArtifact(props.id);
console.log('artifact:', artifact);
console.log(artifact.relightableMedia);

const selectedMedia = ref(artifact.relightableMedia[0].url)

// const selectedMedia = ref('webrti')
function getThumbnailUrl(path) {
  return new URL(path, window.location.origin).toString();
}
</script>

<template>
    <div>
        <OpenLimeViewer :url="getThumbnailUrl(selectedMedia)"/>
        <!-- <NewViewer :url="selectedMedia"/> -->
        
        <p>Relightable Images ({{ artifact.relightableMedia.length }})</p>
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
  border-collapse: collapse;
  margin-top: 1rem;
}

th {
  text-align: left;
  /* padding: 0.5rem; */
  vertical-align: top;
  /* width: 20%; */
  font-weight: bold;
}

td {
  /* padding: 0.5rem; */
}
</style>