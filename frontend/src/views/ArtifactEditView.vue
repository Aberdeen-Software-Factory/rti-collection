<script setup>
import ArtifactEditor from '../components/ArtifactEditor.vue'
import { useArtifact } from '../composables/useArtifact'
import Header from '../components/Header.vue'
import { useRouter } from 'vue-router'
import { ref, watch } from 'vue'
import { useProgressFetch } from '@/composables/useProgressFetch'
import { assembleFormData } from '../backend'
import ProgressHero from '@/components/display/ProgressHero.vue'
import ErrorHero from '@/components/display/ErrorHero.vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

const { id } = defineProps({
    id: String,
})

const { artifact, error } = useArtifact(id)
const router = useRouter()
const editError = ref(null)

const { data, error: uploadError, uploadProgress, downloadProgress, totalProgress, isLoading, progressFetch } = useProgressFetch(new URL(`/artifacts/${id}`, API_BASE_URL))

watch(data, (newData) => {
    if (newData) {
        // TODO: check details but for now assume upload was successful
        router.replace({ name: 'artifact', params: { id: id } })
    }
})

async function handleSubmit(a) {
    console.log("form", a)
    console.log(artifact)

    const username = '';
    const password = prompt("Enter your password:");
    const credentials = btoa(`${username}:${password}`);

    const formData = assembleFormData({
        metadata: a.metadata,
        images: a.imageFiles,
        webrtis: a.webrtiFiles,
        ptms: a.ptmFiles,
    });

    progressFetch({
        method: 'PUT',
        headers: { 'Authorization': `Basic ${credentials}` },
        body: formData
    });
}
</script>

<template>
    <Header :segments="[
        { label: 'Collection', dest: '/' },
        { label: artifact?.metadata.name || 'Artifact', dest: `/artifacts/${artifact?.id}` },
        { label: 'Edit' }
    ]" :title="`Editing: ${artifact?.metadata.name || 'Artifact'}`" />

    <template v-if="isLoading">
        <ProgressHero :progress="totalProgress" />
    </template>

    <template v-else-if="uploadError">
        <ErrorHero :error="uploadError" />
    </template>

    <p v-else-if="error">Error: {{ error }}</p>
    <p v-else-if="editError">Edit Error: {{ editError }}</p>

    <div v-else class="bg-base-300 flex-grow flex">
        <ArtifactEditor v-if="artifact" :artifact="artifact" @submit="handleSubmit">
            <div class="flex w-full gap-2 my-8">
                <RouterLink :to="`/artifacts/${id}`" replace class="btn flex-grow-1">Cancel</RouterLink>
                <button type="submit" class="btn btn-primary flex-grow-1">Save</button>
            </div>
        </ArtifactEditor>
    </div>
</template>