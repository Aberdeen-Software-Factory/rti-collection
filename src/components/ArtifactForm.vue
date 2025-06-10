<script setup>
const title = defineModel('title', { default: '' })
const description = defineModel('description', { default: '' })
const creator = defineModel('creator', { default: '' })
const date = defineModel('date', { default: '' })
const copyright = defineModel('copyright', { default: '' })
const rtis = defineModel('rtis', { default: [] })
const images = defineModel('images', { default: [] }) // New images will be File instances and already uploaded ones will be string urls

const emit = defineEmits(['submit'])

import OpenLimeViewer from '../components/rti/OpenLimeViewer.vue'
import { ref, watch } from 'vue'
import { patchFetchForFiles, restoreOriginalFetch } from '../components/patchFetchForFiles'

import { reactive } from 'vue'

// const artifact = reactive({
//     title: '',
//     description: '',
//     creator: '',
//     date: '',
//     copyright: '',
//     images: [],
// })

const viewerUrl = ref(null)
const fileMap = ref({})

function onFilesSelected(event) {
    const files = Array.from(event.target.files)
    const map = {}
    for (const file of files) {
        map[file.name] = URL.createObjectURL(file) // ✅ store Blob URL, not raw File
    }
    
    fileMap.value = map
    
    const infoBlobUrl = map['info.json']
    if (!infoBlobUrl) {
        alert("Missing info.json")
        return
    }
    
    patchFetchForFiles(map)
    viewerUrl.value = 'info.json'
}

watch(fileMap, (newMap, oldMap) => {
    // Optional: Restore and re-patch if you want clean switching
    restoreOriginalFetch()
    patchFetchForFiles(newMap)
})

function onImageSelected(event) {
    const files = Array.from(event.target.files)
    images.value = [...images.value, ...files] // Add to existing
    event.target.value = null // Allow re-uploading same files if needed
}

function removeImage(index) {
    images.value.splice(index, 1)
}

async function handleSubmit(event) {
    emit('submit', event, {
        title: title.value,
        description: description.value,
        creator: creator.value,
        date: date.value,
        copyright: copyright.value,
        rtis: rtis.value,
        images: images.value,
    })
    event.preventDefault();
    
    return
    event.preventDefault();
    const formData = new FormData()
    formData.append('title', artifact.title)
    formData.append('description', artifact.description)
    formData.append('creator', artifact.creator)
    formData.append('date', artifact.date)
    formData.append('copyright', artifact.copyright)
    
    for (const file of artifact.images) {
        formData.append('images', file) // Note: repeated key name for FastAPI List[UploadFile]
    }
    
    try {
        const response = await fetch('http://localhost:8000/artifacts/', {
            method: 'POST',
            body: formData
        })
        
        if (response.ok) {  // true for 200–299 status codes
            const data = await response.json()
            console.log('Upload successful:', data)
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

function blobUrl(file) {
    if (file instanceof File) {
        return URL.createObjectURL(file);
    } else {
        return file;
    }
}
</script>

<template>
    <form @submit="handleSubmit">
        <h1>Artifact Details</h1>
        <table>
            <tbody>
                <tr>
                    <th><label for="title">Title</label></th>
                    <td><input id="title" v-model="title" type="text" /></td>
                </tr>
                <tr>
                    <th><label for="description">Description</label></th>
                    <td><textarea id="description" v-model="description" rows="3"></textarea></td>
                </tr>
                <tr>
                    <th><label for="creator">Creator</label></th>
                    <td><input id="creator" v-model="creator" type="text" /></td>
                </tr>
                <tr>
                    <th><label for="date">Date</label></th>
                    <td><input id="date" v-model="date" type="text" /></td>
                </tr>
                <tr>
                    <th><label for="copyright">Copyright</label></th>
                    <td><input id="copyright" v-model="copyright" type="text" /></td>
                </tr>
                <tr>
                    <th><label for="images">Still Images</label></th>
                    <td>
                        <input type="button" href="javascript:void(0)" onclick="document.getElementById('file-upload').click()" value="Add Files"/>
                        <input 
                        type="file" 
                        id="file-upload" 
                        style="display: none;" 
                        accept="image/*" 
                        @change="onImageSelected"
                        />
                        <!-- <input
                        id="images"
                        type="file"
                        multiple
                        accept="image/*"
                        @change="onImageSelected"
                        /> -->
                        
                        <!-- Thumbnails -->
                        <div class="thumbnail-list" v-if="images.length">
                            <div
                            class="thumb"
                            v-for="(file, index) in images"
                            :key="file.name"
                            @click="removeImage(index)"
                            title="Click to remove"
                            >
                            <img :src="blobUrl(file)" :alt="file.name" />
                        </div>
                    </div>
                </td>
            </tr>
            <!-- <tr>
                <td colspan="2" style="text-align: right;">
                    <button type="submit">Save</button>
                </td>
            </tr> -->
        </tbody>
    </table>
    <slot></slot>
</form>
</template>

<style scoped>
h1 {
    width: 100%;
}

form {
    max-width: 600px;
}

table {
    width: 100%;
    border-spacing: 0 0.5rem; /* horizontal gap: 0, vertical gap: 1rem */
    border-collapse: separate;
    margin-top: 1rem;
}

th {
    text-align: left;
    vertical-align: top;
    font-weight: bold;
    white-space: nowrap; /* Prevent label wrapping */
    width: 1%; /* Shrink to fit content */
    padding-right: 1rem;
}

td {
    width: auto; /* Take remaining space */
    padding: 0;
}

input[type="text"],
textarea {
    width: 100%; /* Fill available space */
    box-sizing: border-box;
    padding: 6px;
    font-size: 1em;
    border: 1px solid #ccc;
    border-radius: 4px;
    resize: vertical;
}

.thumbnail-list {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 0.5rem;
}

.thumb {
    position: relative;
    width: 80px;
    height: 80px;
    cursor: pointer;
    border: 2px solid #ccc;
    border-radius: 4px;
    overflow: hidden;
}

.thumb img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

</style>