<script setup>
defineProps(['artifact'])
import ArtifactCardImage from './ArtifactCardImage.vue'
</script>

<template>
  <section class="artifact-card">
    <ArtifactCardImage :artifact/>
    <p v-if="artifact.num_rtis > 0" class="rti-badge">RTI</p>
    <div class="card-info">
      <h3>{{ artifact.title }}</h3>
      <p>{{ artifact.date }}</p>
    </div>
  </section>
</template>

<style scoped>
.artifact-card {
  position: relative;
  width:100%;
  display:flex;
  flex-direction:column;
  gap: 10px;
  box-sizing: content-box;
  /* border-radius:10px; */
  /* box-shadow: 0 0 5px #ddd; */
  text-align: left;
  background-color: rgba(0, 0, 0, 0);
  cursor: pointer;
}
.artifact-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: rgba(0, 0, 0, 0.2);
  z-index: 0;
  transform: scale(1);         /* initial scale */
  transition: transform 0.1s ease, opacity 0.1s ease;
  opacity: 0;                  /* hidden by default */
  pointer-events: none;        /* let mouse events pass through */
}

.artifact-card:hover::before {
  transform: scale(1.1);       /* "expand" background visually */
  opacity: 1;                  /* fade in */
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