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
  <div class="form-row">
    <label class="form-label">{{ label }}</label>
    <div class="form-field">
      <select class="form-input" v-model="selected">
        <option disabled value="">Please select</option>
        <option v-for="(option, index) in options" :key="index" :value="option.value">
          {{ option.text }}
        </option>
      </select>
    </div>
  </div>
</template>

<style scoped>
</style>