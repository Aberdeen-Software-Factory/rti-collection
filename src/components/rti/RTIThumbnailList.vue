<script setup>
const props = defineProps(['urls']);
const selectedUrl = defineModel('selectedUrl');
import OpenLimeThumbnail from './OpenLimeThumbnail.vue';
</script>

<template>
    <p>Relightable Images ({{ urls.length }})</p>
    <div class="image-scroller">
        <div class="image-list">
            <OpenLimeThumbnail
            v-for="(url, index) in urls"
            :key="index"
            :url="url"
            :class="{ selected: selectedUrl === url }"
            v-on:click="selectedUrl = url"
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
</style>