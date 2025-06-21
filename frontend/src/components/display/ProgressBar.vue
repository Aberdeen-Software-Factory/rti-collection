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
  
  
  <div class="hero bg-base-200 min-h-screen">
    <div class="hero-content text-center">
      <div class="max-w-md">
        <div class="flex w-52 flex-col gap-4 mx-auto">
          <div class="skeleton h-32 w-full"></div>
          <div class="skeleton h-4 w-28"></div>
          <div class="skeleton h-4 w-full"></div>
          <div class="skeleton h-4 w-full"></div>
        </div>
        <!-- <h1 class="text-5xl font-bold">amdsd</h1> -->
         <slot></slot>
        <p class="py-6">
          Uploading artifact files and info.
        </p>
        <progress :value="progress" max="1" class="progress progress-primary w-84"></progress>
      </div>
    </div>
  </div>
  
  
</template>