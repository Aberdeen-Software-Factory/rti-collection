<script setup>
const props = defineProps(['media']);
const selected = defineModel('selected');

function getThumbnailUrl(path) {
  return new URL(path, "http://localhost:8000/").toString();
}
</script>

<template>
    <div class="image-scroller">
        <div class="image-list">
            <img
            v-for="(rti, index) in media"
            :key="index"
            :src="getThumbnailUrl(rti.thumbnail)"
            :class="{ selected: selected === rti.url }"
            v-on:click="selected = rti.url"
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

img {
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

img:hover {
    transform: scale(1.05);
}

img.selected {
    border-color: #007BFF;
}
</style>