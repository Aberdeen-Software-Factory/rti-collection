<script setup>
import { reactive, onMounted, ref } from 'vue'

import { fetchFiles } from '@/utils';
import JSZip from 'jszip';
import TextInput from './input/TextInput.vue';
import LargeTextInput from './input/LargeTextInput.vue';
import SelectInput from './input/SelectInput.vue';
import TagsInput from './input/TagsInput.vue';
import FilesInput from './input/FilesInput.vue';

import { Artifact } from '@/model/artifact';

const { artifact } = defineProps({
    artifact: {
        type: Artifact,
        default: () => new Artifact(),
    },
});

const isLoading = ref(true);

const ccLicenseOptions = [
  { value: "CC BY",           text: "Attribution (CC BY)" },
  { value: "CC BY-SA",        text: "Attribution-ShareAlike (CC BY-SA)" },
  { value: "CC BY-ND",        text: "Attribution-NoDerivs (CC BY-ND)" },
  { value: "CC BY-NC",        text: "Attribution-NonCommercial (CC BY-NC)" },
  { value: "CC BY-NC-SA",     text: "Attribution-NonCommercial-ShareAlike (CC BY-NC-SA)" },
  { value: "CC BY-NC-ND",     text: "Attribution-NonCommercial-NoDerivs (CC BY-NC-ND)" },
]

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

    const zipFile = new File([zipBlob], "archive.zip", { type: zipBlob.type })
    zippedWebrtis.push(zipFile);
  }
  
  form.webrtiFiles = zippedWebrtis;
  
  // Download image files
  const images = await fetchFiles(artifact.images);
  
  form.imageFiles = images;
  
  isLoading.value = false;
}

onMounted(() => {
    downloadFiles()
})

</script>

<template>
    <h1 v-if="isLoading">Loading...</h1>
    <form v-else @submit.prevent="handleSubmit" class="max-w-2xl mx-auto p-2 w-full">
        <fieldset class="fieldset">
            <legend class="fieldset-legend">Files</legend>
            <FilesInput
                label="Media"
                v-model:images="form.imageFiles"
                v-model:webrtis="form.webrtiFiles"
                v-model:ptms="form.ptmFiles"
            />
        </fieldset>
        <fieldset class="fieldset gap-2">
                        <legend class="fieldset-legend">Metadata</legend>

            <div class="grid gap-2 grid-cols-1 md:[grid-template-columns:auto_1fr]">
    
            <TextInput label="Name" v-model:text="form.metadata.name"/>
            <TagsInput label="Language" v-model="form.metadata.language"/>
            <TagsInput label="Script/Writing System" v-model="form.metadata.script"/>
            <TagsInput label="Archeological Provenance" v-model="form.metadata.provenance"/>
            <TagsInput label="Current Location" v-model="form.metadata.location"/>
            <TagsInput label="Photographer(s)" v-model="form.metadata.photographer"/>
            <TextInput label="Date(s) of Imaging" v-model:text="form.metadata.date"/>
            <LargeTextInput label="Bibliography" v-model:text="form.metadata.bibliography"/>
            <LargeTextInput label="Notes" v-model:text="form.metadata.notes"/>
            <TagsInput label="Keywords" v-model="form.metadata.keywords"/>
            <SelectInput label="Copyright" :options="ccLicenseOptions" v-model:selected="form.metadata.copyright"/>
        </div>

        
    </fieldset>
    <slot></slot>
</form>
</template>

<style scoped>

</style>