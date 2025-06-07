<script setup>
const props = defineProps(['artifact'])
import OpenLimeViewer from './rti/OpenLimeViewer.vue'

console.log(props.artifact)
</script>

<template>
    <div>
        <OpenLimeViewer :url="artifact.relightableMedia[0].url"/>
        <div class="image-scroller">
            <div class="image-list">
                <img
                v-for="(img, index) in artifact.images"
                :key="index"
                :src="img"
                alt="Thumbnail"
                class="thumbnail"
                />
            </div>
        </div>
        <p>{{ artifact.images.length }} media, {{ artifact.relightableMedia.length }} relightable</p>

        <h1>{{ artifact.title }}</h1>
        <p>{{ artifact.description }}</p>
        <p>{{ artifact.creator }}</p>
        <p>{{ artifact.copyright }}</p>
    </div>
</template>

<style scoped>
.image-scroller {
    overflow-x: auto;
    white-space: nowrap;
    padding: 8px;
}

.image-list {
    display: flex;
    flex-direction: row;
    gap: 10px;
}

.thumbnail {
    flex-shrink: 0;
    width: 100px;
    height: 100px;
    object-fit: cover;
    border-radius: 8px;
    cursor: pointer;
    transition: transform 0.2s;
}

.thumbnail:hover {
    transform: scale(1.05);
}
</style>