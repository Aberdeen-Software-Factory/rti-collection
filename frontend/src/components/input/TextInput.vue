<script setup>
const text = defineModel('text')
const props = defineProps({
    label: String,
})
</script>

<template>
    <label class="text-base-content/50 self-baseline">{{ label }}:</label>
    <input
        type="text"
        class="input w-full text-base-content self-baseline"
        v-model="text"
    />
</template>

<style scoped>

</style>