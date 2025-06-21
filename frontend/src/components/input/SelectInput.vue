<script setup>
const selected = defineModel()
const props = defineProps({
  label: String,
  options: {
    type: Array,
    default: () => []
  }
})
</script>

<template>
    <label class="text-sm text-base-content/50 self-baseline">{{ label }}:</label>
    <select class="select self-baseline w-full" v-model="selected">
      <option disabled value="">Please select</option>
      <option v-for="(option, index) in options" :key="index" :value="option.value">
        {{ option.text }}
      </option>
    </select>
</template>
