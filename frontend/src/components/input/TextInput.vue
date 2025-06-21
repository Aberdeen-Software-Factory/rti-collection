<script setup>
const text = defineModel()
const props = defineProps({
    label: String,
})
</script>

<template>
    <label class="text-sm text-base-content/50 self-baseline">{{ label }}:</label>
    <input
        type="text"
        class="input w-full text-base-content self-baseline"
        v-model="text"
    />
</template>

<style scoped>

</style>