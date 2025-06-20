<script setup>
import ArtifactForm from '../components/ArtifactForm.vue';
import { createArtifact } from '../backend.js';
import { useRouter } from 'vue-router'

const router = useRouter()

async function handleSubmit(artifact) {
    try {
        const res = await createArtifact({
            metadata: {
                title: artifact.title,
                description: artifact.description,
                creator: artifact.creator,
                date: artifact.date,
                copyright: artifact.copyright,
            },
            images: artifact.images,
            webrtis: artifact.webrtis,
            ptms: artifact.ptms,
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
    <ArtifactForm
    @submit="handleSubmit"
    ></ArtifactForm>
</template>

<style scoped>
h1 {
    width: 100%;
}

</style>