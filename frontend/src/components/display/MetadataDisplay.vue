<script setup>
const props = defineProps(['metadata'])

import { computed } from 'vue'

import StringField from './StringField.vue';

const displayMetadata = computed(() => {
  return Object.entries(props.metadata).filter(([_, val]) => shouldDisplay(val))
})

const shouldDisplay = (val) => {
  if (val == null) return false           // null or undefined
  if (Array.isArray(val)) return val.length > 0
  if (typeof val === 'string') return val.trim() !== ''
  return true
}

const formatLabel = (key) => key.charAt(0).toUpperCase() + key.slice(1)
</script>

<template>
    <div class="label-value-container">
        <StringField
            v-for="[key, value] in displayMetadata"
            :key="key"
            :label="formatLabel(key)"
            :value="value"
        />
    </div>
</template>

<style scoped>
.label-value-container {
    max-width: 600px;
}
</style>