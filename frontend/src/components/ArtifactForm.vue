<script setup>
import { reactive } from 'vue'

const { defaultValues } = defineProps({
    defaultValues: {
        default: {}
    }
});

const emit = defineEmits(['submit'])

const artifact = reactive({
    // Metadata
    id: defaultValues.id ?? '',
    title: defaultValues.title ?? '',
    description: defaultValues.description ?? '',
    creator: defaultValues.creator ?? '',
    date: defaultValues.date ?? '',
    copyright: defaultValues.copyright ?? '',
    // Media
    images: defaultValues.images ?? [],
    RTIs: defaultValues.RTIs ?? [],
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
    emit('submit', artifact);
    event.preventDefault();
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