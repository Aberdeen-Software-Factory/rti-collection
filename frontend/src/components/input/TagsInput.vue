<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  label: String,
  modelValue: Array // the array of tags
})

const emit = defineEmits(['update:modelValue'])

// Internal text shown in input
const internalText = ref(props.modelValue?.join(', ') || '')

// Update internalText when modelValue changes externally
watch(() => props.modelValue, (newVal) => {
  internalText.value = newVal?.join(', ') || ''
})

// When user finishes typing, parse and emit array
function onBlur() {
  const parsed = internalText.value
  .split(',')
  .map(s => s.trim())
  .filter(Boolean)
  emit('update:modelValue', parsed)
}
</script>

<template>
  <label class="text-base-content/50 self-baseline">{{ label }}:</label>
  <input
    v-model="internalText"
    @blur="onBlur"
    type="text"
    class="input self-baseline w-full"
    title="Enter tags separated by commas"
  />
</template>
