<script setup>
import { reactive, onMounted, ref } from 'vue'

import { fetchFiles } from '@/utils';
import JSZip from 'jszip';
import FilesInput from './input/FilesInput.vue';
import MetadataEditor from './input/MetadataEditor.vue';
import LoadingHero from './display/LoadingHero.vue';
import ErrorHero from './display/ErrorHero.vue';

import { Artifact } from '@/model/artifact';

const { artifact } = defineProps({
    artifact: {
        type: Artifact,
        default: () => new Artifact(),
    },
});

const isLoading = ref(true);
const error = ref(null)

const emit = defineEmits(['submit'])
console.log(artifact)

const form = reactive({
    id: artifact.id,
    metadata: artifact.metadata,

    // Media Files (these are needed as the artifact only contains urls to files on server)
    imageFiles: [],  // .jpg files
    webrtiFiles: [], // .zip files
    ptmFiles: [],    // .ptm files
});


async function handleSubmit(event) {
    emit('submit', form);
    event.preventDefault();
}

async function downloadFiles() {
  // Download RTI files
  const zippedWebrtis = [];
  
  for (const rti of artifact.RTIs) {
    console.log("webrti", rti)
    const files = await fetchFiles(rti.files)
    const zip = new JSZip();
    for (const file of files) {
      zip.file(file.name, file); // Add each file to the ZIP
    }

    const zipBlob = await zip.generateAsync({ type: "blob" }); // or "base64", "uint8array", etc.

    const zipFile = new File([zipBlob], crypto.randomUUID(), { type: zipBlob.type })
    zippedWebrtis.push(zipFile);
  }
  
  form.webrtiFiles = zippedWebrtis;
  
  // Download image files
  const images = await fetchFiles(artifact.images);
  
  form.imageFiles = images;
  
  isLoading.value = false;
}

onMounted(async () => {
    try {
        await downloadFiles() //TODO: convert to composable function
    } catch (err) {
        isLoading.value = false
        error.value = err
    }
})

</script>

<template>
    <template v-if="isLoading">
        <LoadingHero/>
    </template>
    
    <template v-else-if="error">
        <ErrorHero :error="error"/>
    </template>

    <form v-else @submit.prevent="handleSubmit" class="grid max-w-2xl mx-auto p-2 w-full gap-4">
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
