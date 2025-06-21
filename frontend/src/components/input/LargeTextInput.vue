<script setup>
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import { watch } from 'vue'

const text = defineModel()   // Your reactive model prop
const { label } = defineProps({
    label: String,
})

const editor = useEditor({
  content: text.value || '<p></p>',
  extensions: [StarterKit],
  editorProps: {
    attributes: {
      class: 'textarea prose prose-sm text-base-content max-h-80 w-full overflow-y-auto',
    },
  },
  onUpdate({ editor }) {
    text.value = editor.getHTML()
  },
})

// Optional: If `text` changes from outside, update editor content
watch(text, (newVal) => {
  if (editor && editor.value.getHTML() !== newVal) {
    editor.commands.setContent(newVal || '<p></p>')
  }
})
</script>

<template>
    <label class="text-sm text-base-content/50 self-baseline">{{ label }}:</label>
    <editor-content :editor="editor" class="self-baseline"/>
</template>

<style scoped>
:deep(.prose p) {
  margin-top: 0;
  margin-bottom: 0;
}
</style>