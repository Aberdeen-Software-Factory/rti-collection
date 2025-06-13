<script setup>
import OpenLimeViewer from '../components/rti/OpenLimeViewer.vue'
import { ref, watch } from 'vue'
import { patchFetchForFiles, restoreOriginalFetch } from '../components/patchFetchForFiles'
import { createArtifact } from '../backend.js';
import { reactive } from 'vue'

const artifact = reactive({
    // metadata
    title: '',
    description: '',
    creator: '',
    date: '',
    copyright: '',
    // media
    images: [],
    RTIs: [],
})


function onImageSelected(event) {
    const files = Array.from(event.target.files)
    artifact.images = [...artifact.images, ...files]
    event.target.value = null
}

function removeImage(index) {
    artifact.images.splice(index, 1)
}

function onRTISelected(event) {
    const files = Array.from(event.target.files)
    artifact.RTIs = [...artifact.RTIs, files]
    event.target.value = null
}

function removeRTI(index) {
    artifact.RTIs.splice(index, 1);
}

async function handleSubmit(event) {
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

function blobUrl(file) {
    return URL.createObjectURL(file);
}
</script>

<template>
    <h1>Upload Artifact</h1>
    <form @submit.prevent="handleSubmit">
        <div class="form-row">
            <label class="form-label" for="title">Title</label>
            <div class="form-field">
                <input id="title" v-model="artifact.title" type="text" />
            </div>
        </div>
        
        <div class="form-row">
            <label class="form-label" for="description">Description</label>
            <div class="form-field">
                <textarea id="description" v-model="artifact.description" rows="3"></textarea>
            </div>
        </div>
        
        <div class="form-row">
            <label class="form-label" for="creator">Creator</label>
            <div class="form-field">
                <input id="creator" v-model="artifact.creator" type="text" />
            </div>
        </div>
        
        <div class="form-row">
            <label class="form-label" for="date">Date</label>
            <div class="form-field">
                <input id="date" v-model="artifact.date" type="text" />
            </div>
        </div>
        
        <div class="form-row">
            <label class="form-label" for="copyright">Copyright</label>
            <div class="form-field">
                <input id="copyright" v-model="artifact.copyright" type="text" />
            </div>
        </div>
        
        <div class="form-row">
            <label class="form-label" for="images">Images</label>
            <div class="form-field">
                <input
                id="images"
                type="file"
                multiple
                accept="image/*"
                @change="onImageSelected"
                />
                <div class="thumbnail-list" v-if="artifact.images.length">
                    <div
                    class="thumb"
                    v-for="(file, index) in artifact.images"
                    :key="file.name"
                    @click="removeImage(index)"
                    title="Click to remove"
                    >
                    <img :src="blobUrl(file)" :alt="file.name" />
                </div>
            </div>
        </div>
    </div>
    <!-- RTI upload -->
    <div class="form-row">
        <label class="form-label" for="RTIs">RTIs</label>
        <div class="form-field">
            <input
            id="RTIs"
            type="file"
            multiple
            @change="onRTISelected"
            />
            <div class="thumbnail-list" v-if="artifact.RTIs.length">
                    <div
                    class="thumb"
                    v-for="(files, index) in artifact.RTIs"
                    :key="index"
                    @click="removeRTI(index)"
                    title="Click to remove"
                    >
                    <p>{{ files.length }} files</p>
                    <!-- <img :src="blobUrl(file)" :alt="file.name" /> -->
                </div>
            </div>
        </div>
    </div>
    
    <div class="form-row" style="justify-content: flex-end;">
        <button type="submit">Upload</button>
    </div>
</form>
</template>

<style scoped>
h1 {
    width: 100%;
}

/* form {
max-width: 600px;
} */

.form-row {
    display: flex;
    flex-wrap: wrap;
    margin-bottom: 1em;
}

.form-label {
    flex: 0 0 150px;
    max-width: 150px;
    font-weight: bold;
    padding-right: 1em;
    box-sizing: border-box;
}

.form-field {
    flex: 1;
    min-width: 0;
}

@media (max-width: 600px) {
    .form-row {
        flex-direction: column;
    }
    
    .form-label {
        flex: 0 0 0;
        max-width: 100%;
        margin-bottom: 0.25em;
    }
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