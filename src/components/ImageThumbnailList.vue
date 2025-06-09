<script setup>
const props = defineProps(['urls']);
const selectedUrl = defineModel('selectedUrl');
</script>

<template>
    <p>Still Images ({{ urls.length }})</p>
    <div class="image-scroller">
        <div class="image-list">
            <img
            v-for="(url, index) in urls"
            :key="index"
            :src="url"
            :class="{ selected: selectedUrl === url }"
            v-on:click="selectedUrl = url"
            class="thumbnail"
            />
        </div>
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
    border: 2px solid transparent;
    border-radius: 8px;
    /* overflow: hidden; */
    cursor: pointer;
    transition: transform 0.2s;
}

.thumbnail:hover {
    transform: scale(1.05);
}

.thumbnail.selected {
    border-color: #007BFF;
}
</style>