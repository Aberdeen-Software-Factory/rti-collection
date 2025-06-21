<script setup>
const text = defineModel('text')
const props = defineProps({
    label: String,
})
</script>

<template>
    <div class="form-row">
        <label class="form-label" for="title">{{ label }}</label>
        <div class="form-field">
            <textarea
                class="form-input"
                type="text"
                v-model="text"
            />
        </div>
    </div>
</template>

<style scoped>

.badge {
  display: inline-block;
  background-color: #007bff;
  color: white;
  padding: 0.2em 0.5em;
  margin-right: 0.3em;
  border-radius: 0.3em;
  font-size: 0.85em;
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