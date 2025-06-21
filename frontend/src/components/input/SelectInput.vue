<script setup>
const selected = defineModel('selected')
const props = defineProps({
  label: String,
  options: {
    type: Array,
    default: () => []
  }
})
</script>

<template>
    <label class="label grow-1">{{ label }}</label>
    <select class="select" v-model="selected">
      <option disabled value="">Please select</option>
      <option v-for="(option, index) in options" :key="index" :value="option.value">
        {{ option.text }}
      </option>
    </select>
</template>
