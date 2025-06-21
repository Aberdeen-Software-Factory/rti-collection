<script setup>
const text = defineModel('text')
const props = defineProps({
    label: String,
})
</script>

<template>
    <label class="label self-baseline">{{ label }}</label>
    <textarea
      type="text"
      class="textarea self-baseline text-base-content w-full"
      v-model="text"
    />
</template>
