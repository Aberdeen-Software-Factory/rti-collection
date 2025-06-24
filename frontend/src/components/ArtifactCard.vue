<script setup>
import ArtifactCardImage from './ArtifactCardImage.vue'

/**
 * @typedef {import('../model/artifact').ArtifactPreview} ArtifactPreview
 */

/** @type {{ artifact: ArtifactPreview }} */
const { artifact } = defineProps({
  artifact: Object,
})
</script>

<template>
  <section class="artifact-card grid">
    <!-- <ArtifactCardImage :artifact/> -->
    <div 
        class="h-full w-full aspect-square cursor-pointer overflow-hidden border border-base-300 bg-neutral content-center place-content-center text-center text-neutral-content"
    >
        <img v-if="artifact.thumbnailURL"
            :src="artifact.thumbnailURL"
            class="h-full w-full object-cover transition-transform duration-300 ease-in-out"
        />
        <p v-else class="transition-transform duration-300 ease-in-out">No Image</p>
    </div>
    <p v-if="artifact.RTICount > 0" class="rti-badge">RTI</p>
    <div class="card-info">
      <h3 class="text-lg">{{ artifact?.metadata.name }}</h3>
      <p>{{ artifact?.metadata.date }}</p>
    </div>
  </section>
</template>

<style scoped>
.artifact-card:hover ::v-deep img,
.artifact-card:hover ::v-deep p {
  transform: scale(1.10);
}
</style>