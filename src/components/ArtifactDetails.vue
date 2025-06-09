<script setup>
const props = defineProps(['artifact'])
import OpenLimeViewer from './rti/OpenLimeViewer.vue'
import ImageThumbnailList from './ImageThumbnailList.vue';
import ArtifactThumbnailList from './ArtifactThumbnailList.vue';

import { ref } from 'vue'

console.log(props.artifact)
const selectedMedia = ref(props.artifact.relightableMedia[0].url)
// const selectedMedia = ref('webrti')
</script>

<template>
    <div>
        <OpenLimeViewer :url="selectedMedia"/>
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
        <p>{{ artifact.description }}</p>
        <p>Creator: {{ artifact.creator }}</p>
        <p>{{ artifact.date }}</p>
        <p>{{ artifact.copyright }}</p>
    </div>
</template>

<style scoped>
</style>