<script setup>
defineProps(['artifact'])

function getThumbnail(artifact) {
  if (artifact.relightableMedia.length > 0) {
    return artifact.relightableMedia[0].thumbnail;
  } else {
    return "";
  }
}
</script>

<template>
  <!-- <img v-bind:src="getThumbnail(artifact)"/> -->
  <img v-bind:src="'http://localhost:8000' + artifact.thumbnail"/>
</template>

<style scoped>
img {
  aspect-ratio: 1/1;
  width:100%;
  border-radius:5px;
  cursor:pointer;
  opacity:0.9;
  transition: opacity 0.2s;
  object-fit: cover;
}
img:hover{
  opacity:1;
}
</style>