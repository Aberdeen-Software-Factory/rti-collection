<script setup>
import { reactive } from 'vue'
import FilesInput from '@/components/input/FilesInput.vue';
import MetadataEditor from '@/components/input/MetadataEditor.vue';
import Metadata from '@/models/Metadata';

const props = defineProps({
    defaultMetadata: {
        type: Object,
        default: () => new Metadata(),
    },
    defaultImageFiles: {
        type: Array,
        default: () => []
    },
    defaultZipFiles: {
        type: Array,
        default: () => []
    },
});

const emit = defineEmits(['submit'])

const form = reactive({
    metadata: props.defaultMetadata,
    imageFiles: props.defaultImageFiles,  // .jpg files
    webrtiFiles: props.defaultZipFiles, // .zip files
    ptmFiles: [],    // .ptm files
});

async function handleSubmit(event) {
    emit('submit', form);
    event.preventDefault();
}
</script>

<template>
    <form @submit.prevent="handleSubmit" class="grid max-w-2xl mx-auto p-2 w-full gap-4">
        <fieldset class="fieldset">
            <!-- <legend class="fieldset-legend text-2xl">Files</legend> -->
            
        </fieldset>
        <fieldset class="fieldset gap-2">
                        
            <!-- <legend class="fieldset-legend text-2xl">Metadata</legend> -->

            <div class="grid gap-x-4 gap-y-2 grid-cols-1 md:[grid-template-columns:auto_1fr]">
                <label class="text-sm text-base-content/50 self-baseline">Files:</label>
                <FilesInput
                    label="Media"
                    v-model:images="form.imageFiles"
                    v-model:webrtis="form.webrtiFiles"
                    v-model:ptms="form.ptmFiles"
                    class="mb-4"
                />
                
                <MetadataEditor v-model="form.metadata"/>
            </div>

        
    </fieldset>
    <slot></slot>
</form>
</template>
