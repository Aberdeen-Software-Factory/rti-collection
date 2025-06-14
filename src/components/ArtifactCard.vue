<script setup>
defineProps(['artifact'])
import ArtifactCardImage from './ArtifactCardImage.vue'
</script>

<template>
  <section class="artifact-card">
    <ArtifactCardImage :artifact/>
    <p v-if="artifact.RTICount > 0" class="rti-badge">RTI</p>
    <div class="card-info">
      <h3>{{ artifact.title == '' ? '--' : artifact.title }}</h3>
      <p>{{ artifact.date }}</p>
      <p>{{ artifact.imageCount + artifact.RTICount }} images</p>
    </div>
  </section>
</template>

<style scoped>
.artifact-card {
  height: 100%;
  position: relative;
  /* background-color: white; */
  cursor: pointer;
  /* overflow: hidden; */
  z-index: 0;
  transition: box-shadow 0.3s ease;
}

.artifact-card::before {
  content: '';
  position: absolute;
  inset: -10px; /* expands evenly in all directions */
  background: rgba(0, 0, 0, 0.2);
  border-radius: inherit;
  opacity: 0;
  transition: opacity 0.2s ease;
  z-index: -1; /* put it behind the content */
}

.artifact-card:hover::before {
  opacity: 1;
}
/* .artifact-card:hover {
border: 0cap;
background-color: rgba(0, 0, 0, 0.2);
} */

.card-info {
  z-index: 10;
}

.rti-badge {
  position: absolute;
  top: 0px;
  left: 0px;
  aspect-ratio: 1/1;
  padding: 6px;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 2;
  font-size: 0.75rem;    /* smaller size */
  font-weight: bold;
}

.artifact-card:hover ::v-deep img {
  transform: scale(1.05);
}

h3 {
  font-weight: bold;
}
</style>