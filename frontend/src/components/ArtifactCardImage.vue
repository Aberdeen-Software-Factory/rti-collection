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
   <div class="img-wrapper">
    <img :src="artifact.thumbnailURL"/>
  </div>
</template>

<style scoped>
.img-wrapper {
  display: flex;
  overflow: hidden;
  justify-content: center;
  align-items: center;
  /* border-radius: 5px; */
  width: 100%;
  aspect-ratio: 1.3 / 1;
  background-color: rgb(255, 255, 255, 0.2);

  border: 1px solid rgb(0, 0, 0, 0.5);
  box-sizing: border-box;
}

img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
  cursor: pointer;
  display: block;
  
  /* border-radius removed here because wrapper handles it */
}


</style>