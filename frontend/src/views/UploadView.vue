<script setup>
import ArtifactEditor from '@/components/ArtifactEditor.vue';
import { assembleFormData, createArtifact } from '../backend.js';
import { useRouter } from 'vue-router'
import { useProgressFetch } from '@/composables/useProgressFetch';
import { watch, ref } from 'vue';
import ProgressHero from '@/components/display/ProgressHero.vue';
import Header from '@/components/Header.vue';
import ErrorHero from '@/components/display/ErrorHero.vue';

const router = useRouter()
const { data, error, uploadProgress, downloadProgress, totalProgress, isLoading, progressFetch } = useProgressFetch(new URL('/api/artifacts', window.location.origin))

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
    window.scrollTo({ top: 0, behavior: 'smooth' })
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
    <Header
        :segments="[
        { label: 'Collection', dest: '/'},
        { label: 'Upload' }
        ]"
        title="Upload Artifact"
    />
    
    <div v-if="data">
        <div class="hero bg-base-200 min-h-screen">
            <div class="hero-content text-center">
                <div class="max-w-md">
                    <h1 class="text-5xl font-bold">Success</h1>
                    <slot></slot>
                    <p class="py-6">
                        Artifact uploaded.
                    </p>
                    <div class="flex gap-2">
                        <RouterLink :to="`/artifacts/${data.artifact_id}`" class="btn btn-primary w-40">View</RouterLink>
                        <button @click="reset" class="btn btn-neutral w-40">Upload Another</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <template v-else-if="error">
        <ErrorHero :error="error"/>
    </template>

    <template v-else-if="isLoading" >
        <ProgressHero :progress="totalProgress"/>
    </template>
    
    <div v-else class="bg-base-200">
        
        <!-- <fieldset class="fieldset bg-base-200 border-base-300 rounded-box w-lg border p-4">
            <legend class="fieldset-legend">Metadata</legend>
            
            <MetadataEditor v-model="d"/>
        </fieldset> -->
        
        <ArtifactEditor
        class=""
        @submit="handleSubmit"
        >
        <button type="submit" class="btn btn-primary my-6 w-full">Upload</button>
    </ArtifactEditor>
</div>
</template>

<style scoped>
h1 {
    width: 100%;
}

</style>