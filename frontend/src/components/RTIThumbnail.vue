<script setup>
const props = defineProps(['rti', 'selected']);

function getThumbnailURL(rti) {
    return rti.files.find(url => url.endsWith('plane_0.jpg'))
}
</script>

<template>
    <div class="thumbnail clickable">
        <img v-if="getThumbnailURL(rti)" :src="getThumbnailURL(rti)"/> <!-- TODO: Inefficient double function call -->
        <div v-else class="placeholder-container">
            <p>RTI Image</p>
            <p class="id">No Preview</p>
            <p v-if="rti.id" class="id">{{ rti.id }}</p>
        </div>
    </div>
</template>

<style scoped>
.placeholder-container {
    padding: 5px;
    overflow-wrap: anywhere;
    max-width: 100%;
}

.id {
    font-size: 0.5rem;
    overflow: hidden;
}

img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
</style>