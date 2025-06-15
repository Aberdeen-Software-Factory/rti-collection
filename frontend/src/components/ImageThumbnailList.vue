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
            class="thumbnail clickable"
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