<script setup>
const props = defineProps(['id'])
const RTIs = defineModel('RTIs')

import OpenLimeViewer from './rti/OpenLimeViewer.vue'

async function fetchArtifact(id) {
  try {
    const res = await fetch(`http://localhost:8000/artifacts/${id}`)  // replace with your API URL
    if (!res.ok) throw new Error('Failed to fetch artifact')
    RTIs.value = (await res.json()).artifact.relightableMedia
  } catch (error) {
    console.error(error)
  }
}

async function deleteRTI(artifactID, rtiID) {
    try {
        const response = await fetch(`http://localhost:8000/artifacts/${artifactID}/rti/${rtiID}`, {
            method: 'DELETE'
        })
        
        if (response.ok) {  // true for 200–299 status codes
            const data = await response.json()
            console.log('Upload successful:', data)

            fetchArtifact(props.id)
        } else {
            console.log('Upload failed with status:', response.status)
            // optionally parse error JSON:
            try {
                const errorData = await response.json()
                console.log('Error details:', errorData)
            } catch {
                // no JSON body
            }
        }
    } catch (error) {
        console.error('Upload failed:', error)
    }
}

async function onRTISelected(event) {
    const files = Array.from(event.target.files)
    event.target.value = null
    
    console.log(files)
    const formData = new FormData()
    
    formData.append('metadata', '{ "title": "smtg" }')
    for (const file of files) {
        formData.append('files', file) // Note: repeated key name for FastAPI List[UploadFile]
    }
    
    console.log(formData)
    
    try {
        const response = await fetch(`http://localhost:8000/artifacts/${props.id}/rti`, {
            method: 'POST',
            body: formData
        })
        
        if (response.ok) {  // true for 200–299 status codes
            const data = await response.json()
            console.log('Upload successful:', data)

            fetchArtifact(props.id)
        } else {
            console.log('Upload failed with status:', response.status)
            // optionally parse error JSON:
            try {
                const errorData = await response.json()
                console.log('Error details:', errorData)
            } catch {
                // no JSON body
            }
        }
    } catch (error) {
        console.error('Upload failed:', error)
    }
}
</script>

<template>
    <input 
    type="file" 
    id="rti-upload"
    multiple
    @change="onRTISelected"
    />
    <!-- Thumbnails -->
    <div class="thumbnail-list" v-if="RTIs.length">
        <div
        class="thumb"
        v-for="(rti, index) in RTIs"
        :key="rti.url"
        @click="removeImage(index)"
        title="Click to remove"
        >
        <p>{{ rti.id }}</p>
        <p>{{ rti.url }}</p>
        <button @click="() => deleteRTI(id, rti.id)">Delete</button>
        <OpenLimeViewer :url="'http://localhost:8000' + rti.url"/>
        <!-- <img :src="blobUrl(file)" :alt="file.name" /> -->
    </div>
</div>
</template>

<style scoped>
</style>