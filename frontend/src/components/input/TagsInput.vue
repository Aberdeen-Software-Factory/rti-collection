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
<div class="form-row">
    <label class="form-label">{{ label }}</label>
    <div class="form-field">
      <input
        type="text"
        v-model="internalText"
        @blur="onBlur"
        placeholder="Enter tags separated by commas"
        title="Enter tags separated by commas"
      />
    </div>
  </div>
</template>

<style scoped>

.form-input {
  width: 100%;
  box-sizing: border-box;
  padding: 6px;
  font-size: 1em;
  border: 1px solid #ccc;
  border-radius: 4px;
}

input[type="text"],
textarea {
    width: 100%; /* Fill available space */
    box-sizing: border-box;
    padding: 6px;
    font-size: 1em;
    border: 1px solid #ccc;
    border-radius: 4px;
    resize: vertical;
}
</style>