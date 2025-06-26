<script setup>
import ArtifactPreview from '@/models/ArtifactPreview';

/** @type {{ artifact: ArtifactPreview }} */
const { artifact } = defineProps({
  artifact: Object,
})
</script>

<template>
  <section class="artifact-card grid">
    <div 
        class="rounded-box h-full w-full aspect-square cursor-pointer overflow-hidden border border-base-300 bg-neutral content-center place-content-center text-center text-neutral-content"
    >
        <img v-if="artifact.thumbnail"
            :src="artifact.thumbnail"
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
.artifact-card:hover :deep(img),
.artifact-card:hover :deep(p) {
  transform: scale(1.10);
}
</style>