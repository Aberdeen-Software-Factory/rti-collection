<script setup>
defineProps(['artifact'])

function getThumbnail(artifact) {
  return artifact.relightableMedia[0].thumbnail;
}
</script>

<template>
  <img v-bind:src="getThumbnail(artifact)"/>
</template>

<style scoped>
img {
  aspect-ratio: 1/1;
  width:100%;
  border-radius:5px;
  cursor:pointer;
  opacity:0.9;
  transition: opacity 0.2s;
}
img:hover{
  opacity:1;
}
</style>