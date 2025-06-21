<script setup>
import { defineProps } from 'vue'

// Accept a value between 0 and 1
const props = defineProps({
  progress: {
    type: Number,
    default: 0,
  },
})
</script>

<template>
  <slot></slot>
  <progress :value="progress" max="1" class="w-full h-4"></progress>
</template>