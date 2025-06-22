<script setup>
import ArtifactEditor from '../components/ArtifactEditor.vue'
import { useArtifact } from '../composables/artifact'
import Header from '../components/Header.vue'
import { updateArtifact } from '../backend'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

const { id } = defineProps({
    id: String,
})

const { artifact, error } = useArtifact(id)
const router = useRouter()
const editError = ref(null)

async function handleSubmit(a) {
    console.log("form", a)
    console.log(artifact)
    
    // event.preventDefault();
    
    try {
        console.log(a)
        const res = await updateArtifact(a.id, {
        metadata: a.metadata,
        images: a.imageFiles,
        webrtis: a.webrtiFiles,
        ptms: a.ptmFiles,
        });
        console.log(res);
        
        router.replace({ name: 'artifact', params: { id: id } })
    } catch (error) {
        editError.value = error
        console.log(error)
    }
}
</script>

<template>
    <Header
        :segments="[
        { label: 'Collection', dest: '/'},
        { label: artifact?.metadata.name || 'Artifact', dest: `/artifacts/${artifact?.id}` },
        { label: 'Edit' }
        ]"
        :title="`Editing: ${artifact?.metadata.name || 'Artifact'}`"
    />

    <p v-if="error">Error: {{ error }}</p>
    <p v-if="editError">Edit Error: {{ editError }}</p>

    <ArtifactEditor
        v-if="artifact"
        :artifact="artifact"
        @submit="handleSubmit"
    >
        <RouterLink :to="`/artifacts/${id}`" replace class="btn">Cancel</RouterLink>
        <button type="submit" class="btn btn-primary">Save</button>
    </ArtifactEditor>
</template>