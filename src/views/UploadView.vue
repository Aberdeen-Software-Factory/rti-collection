<script setup>
import ArtifactForm from '../components/ArtifactForm.vue';
import { createArtifact } from '../backend.js';

async function handleSubmit(artifact) {
    const res = await createArtifact({
        metadata: {
            title: artifact.title,
            description: artifact.description,
            creator: artifact.creator,
            date: artifact.date,
            copyright: artifact.copyright,
        },
        images: artifact.images,
        RTIs: artifact.RTIs,
    });

    console.log(res);
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