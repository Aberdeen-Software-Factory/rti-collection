<script setup>
const props = defineProps(['rti', 'selected']);

function getThumbnailURL(path) {
    return new URL(path, "http://localhost:8000/").toString();
}
</script>

<template>
    <div class="thumbnail clickable">
        <img v-if="rti.thumbnail" :src="getThumbnailURL(rti.thumbnail)"/>
        <div v-else class="placeholder-container">
            <p>No Preview</p>
            <p v-if="rti.id" class="id">RTI ID: {{ rti.id }}</p>
        </div>
    </div>
</template>

<style scoped>


.placeholder-container {
    padding: 5px;
    overflow-wrap: anywhere;
}

.id {
    font-size: 0.5rem;
}

img {
    width: 100%;
    height: 100%;
}
</style>