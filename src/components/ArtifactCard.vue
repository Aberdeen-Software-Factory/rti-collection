<script setup>
    defineProps(['artifact'])
    import ArtifactCardImage from './ArtifactCardImage.vue'
</script>

<template>
<section class="artifact-card">
    <ArtifactCardImage/>
    <h1>{{ artifact.title }}</h1>
    <p>{{ artifact.description }}</p>
    <p>{{ artifact.copyright }}</p>
    <p>{{ artifact.creator }}</p>
</section>
</template>

<style scoped>
.artifact-card {
  width:100%;
  display:flex;
  flex-direction:column;
  border-radius:10px;
  box-shadow: 0 0 5px #ddd;
  padding:15px;
  text-align: left;
}
</style>