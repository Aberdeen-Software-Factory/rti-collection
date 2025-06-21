<script setup>
import ArtifactEditor from '../components/ArtifactEditor.vue';
import { assembleFormData, createArtifact } from '../backend.js';
import { useRouter } from 'vue-router'
import { useProgressFetch } from '@/composables/progressFetch';
import { watch } from 'vue';
import ProgressBar from '@/components/display/ProgressBar.vue';

const router = useRouter()
const { data, error, uploadProgress, downloadProgress, totalProgress, isLoading, progressFetch } = useProgressFetch(new URL('/artifacts', 'http://localhost:8000'))

watch([data, error], ([newData, newError]) => {
  if (newError) {
    console.error('Error:', newError)
  } else if (newData) {
    console.log('Data:', newData)
  }
})

async function handleSubmit(uploadForm) {
    console.log(uploadForm)

    const username = '';
    const password = prompt("Enter your password:");
    const credentials = btoa(`${username}:${password}`);

    const formData = assembleFormData({
        metadata: uploadForm.metadata,
        images: uploadForm.imageFiles,
        webrtis: uploadForm.webrtiFiles,
        ptms: uploadForm.ptmFiles,
    });

    progressFetch({
        method: 'POST',
        headers: { 'Authorization': `Basic ${credentials}` },
        body: formData
    });

    return;
    try {
        const res = await createArtifact({
            metadata: uploadForm.metadata,
            images: uploadForm.imageFiles,
            webrtis: uploadForm.webrtiFiles,
            ptms: uploadForm.ptmFiles,
        });
        
        console.log(res);
        router.push("/");
    } catch (error) {
        console.log(error);
        alert('Unable to upload artifact.')
    }
}

function reset() {
    data.value = null
    error.value = null
}
</script>

<template>
    <h1>Upload Artifact</h1>

    <div v-if="data || error" >
        <ProgressBar :progress="totalProgress">
            <p>Data: {{ data }}</p>
            <p>Error: {{ error }}</p>
            <p>Upload Progress: {{ uploadProgress }}</p>
            <p>Download Progress: {{ downloadProgress }}</p>
            <p>Total Progress: {{ totalProgress }}</p>
        </ProgressBar>
    </div>

    <ArtifactEditor
        v-else
        class=""
        @submit="handleSubmit"
    >
        <button type="submit" class="btn btn-primary my-6 w-full">Upload</button>
    </ArtifactEditor>
</template>

<style scoped>
h1 {
    width: 100%;
}

</style>