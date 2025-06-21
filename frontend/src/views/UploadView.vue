<script setup>
import ArtifactEditor from '../components/ArtifactEditor.vue';
import { createArtifact } from '../backend.js';
import { useRouter } from 'vue-router'

const router = useRouter()

async function handleSubmit(uploadForm) {
    console.log(uploadForm)

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
</script>

<template>
    <h1>Upload Artifact</h1>
    <ArtifactEditor
    @submit="handleSubmit"
    >
        <button type="submit">Upload</button>
    </ArtifactEditor>
</template>

<style scoped>
h1 {
    width: 100%;
}

</style>