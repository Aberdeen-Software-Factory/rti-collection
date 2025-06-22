<script setup>
/**
 * @typedef {Object} ImageOption
 * @property {string} thumbnail - URL of the thumbnail
 * @property {string} value - Actual value represented by the image
 */

const props = defineProps({
  options: {
    type: Array,
    required: true,
  },
});

const selected = defineModel();

</script>

<template>
  <div class="flex flex-nowrap w-full overflow-x-auto gap-4">
    <div 
         v-for="(option, index) in options"
        class="size-30 md:size-40 aspect-1 flex-shrink-0 cursor-pointer overflow-hidden"
        :class="{ 'border-4 border-primary': selected === option.value }"
    >
        <img
            :key="index"
            :src="option.thumbnail"
            class="h-full w-full object-cover transition-transform duration-300 ease-in-out hover:scale-110"
            @click="selected = option.value"
        />
    </div>
  </div>
</template>