<script setup>
const props = defineProps({
    label: String,
    value: [String, Array],
})
</script>

<template>
    <div class="form-row">
        <label class="form-label">{{ label }}</label>
        <div class="form-field">
            <template v-if="Array.isArray(value)">
                <template v-for="(item, i) in value" :key="i">
                    <!-- TODO: on click search filtering clicked property -->
                    <span class="link-style">{{ item }}</span> 
                    <span v-if="i < value.length - 1">, </span>
                </template>
            </template>
            <p
            v-else-if="['bibliography', 'notes'].includes(label?.toLowerCase() || '')"
            :class="'prose prose-base text-base-content'"
            v-html="value"
            ></p>
            <p v-else>{{ value }}</p>
        </div>
    </div>
</template>

<style scoped>
.form-row {
    display: flex;
    flex-wrap: wrap;
    margin-bottom: 1em;
}

.form-label {
    flex: 0 0 150px;
    max-width: 150px;
    font-weight: bold;
    padding-right: 1em;
    box-sizing: border-box;
}

.form-field {
    flex: 1;
    min-width: 0;
}

.badge {
  display: inline-block;
  background-color: #007bff;
  color: white;
  padding: 0.2em 0.5em;
  margin-right: 0.3em;
  border-radius: 0.3em;
  font-size: 0.85em;
}
</style>