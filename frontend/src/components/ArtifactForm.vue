<script setup>
import { reactive } from 'vue'
import JSZip from "jszip";
import ZipPreview from './ZipPreview.vue'

const { defaultValues } = defineProps({
    defaultValues: {
        default: {}
    }
});

const emit = defineEmits(['submit'])

const form = reactive({
    // Metadata
    id: defaultValues.id ?? '',
    title: defaultValues.title ?? '',
    description: defaultValues.description ?? '',
    creator: defaultValues.creator ?? '',
    date: defaultValues.date ?? '',
    copyright: defaultValues.copyright ?? '',
    // Media
    images: defaultValues.images ?? [], // .jpg files
    webrtis: defaultValues.RTIs ?? [],  // .zip files
    ptms: defaultValues.ptms ?? [],     // .ptm files
})

function getFileExtension(file) {
    const parts = file.name.split('.');
    return parts.length > 1 ? parts.pop().toLowerCase() : '';
}

function onImageSelected(event) {
    const files = Array.from(event.target.files)

    for (const file of files) {
        switch (getFileExtension(file)) {
            case "jpg":
                form.images = [...form.images, file]
                break;
            case "zip":
                form.webrtis = [...form.webrtis, file]
                break;
            case "ptm":
                form.ptms = [...form.ptms, file]
                break;
            default:
                console.log(`Unsupported file uploaded: ${file.name}`)
        }
    }

    event.target.value = null
}

function removeImage(index) {
    form.images.splice(index, 1)
}

function onRTISelected(event) {
    const files = Array.from(event.target.files)
    form.webrtis = [...form.webrtis, files]
    event.target.value = null
}

function removeRTI(index) {
    form.webrtis.splice(index, 1);
}

function removePtm(index) {
    form.ptms.splice(index, 1);
}

async function handleSubmit(event) {
    emit('submit', form);
    event.preventDefault();
}

function getPlane0(files) {
    console.log(files)
    return files.find(file => file.name === 'plane_0.jpg');
}

function blobUrl(file) {
    if (file instanceof File) {
        return URL.createObjectURL(file);
    } else {
        return file;
    }
}

async function listZipContents(zipFile, filename="plane_0.jpg") {
  const zip = await JSZip.loadAsync(zipFile); // Load the ZIP contents

  

//   const fileNames = Object.keys(zip.files); // List of file paths/names in the ZIP

//   fileNames.forEach(name => {
//     const file = zip.files[name];
//     console.log({
//       name,
//       isDirectory: file.dir,
//       compressedSize: file._data?.compressedSize, // may be undefined
//       uncompressedSize: file._data?.uncompressedSize, // may be undefined
//     });
//   });

  const file = zip.files[filename];
    console.log(file)
  const blob = await file.async("blob"); // Extract the file as a Blob
  const url = URL.createObjectURL(blob); // Create a temporary object URL
  console.log(url)
  return url;

}

</script>

<template>
    <form @submit.prevent="handleSubmit">
        <div class="form-row">
            <label class="form-label" for="title">Title</label>
            <div class="form-field">
                <input id="title" v-model="form.title" type="text" />
            </div>
        </div>

        <div class="form-row">
            <label class="form-label" for="images">Files</label>
            <div class="form-field">
                <input
                id="images"
                type="file"
                accept=".jpg, .zip, .ptm"
                multiple
                @change="onImageSelected"
                />
            </div>
    </div>
        
        <div v-if="form.ptms.length" class="form-row">
            <label class="form-label" for="images"></label>
            <div class="form-field">
                <h4>Polynomial Texture Map (.ptm) Files:</h4>
                <div class="thumbnail-list" v-if="form.ptms.length">
                    <div
                    class="thumb"
                    v-for="(file, index) in form.ptms"
                    :key="file.name"
                    @click="removePtm(index)"
                    title="Click to remove"
                    >
                    <p>{{ file.name }}</p>
                    <!-- <img :src="blobUrl(file)" :alt="file.name" /> -->
                </div>
            </div>
        </div>
        </div>

        <!-- RTI upload -->
        <div v-if="form.webrtis.length" class="form-row">
            <label class="form-label" for="RTIs"></label>
            <div class="form-field">
                <!-- <input id="RTIs" type="file" multiple @change="onRTISelected"/> -->
                <h4>Relight Web Format Files:</h4>
                <div class="thumbnail-list" v-if="form.webrtis.length">
                    <div class="thumb" v-for="(files, index) in form.webrtis" :key="index" @click="removeRTI(index)" title="Click to remove">
                        <p>{{ files.length }} files</p>
                        <!-- <img :src="blobUrl(getPlane0(files))" /> -->
                        <ZipPreview :zipFile="files" :filename="'plane_0.jpg'"/>
                    </div>
                </div>
            </div>
        </div>
        
        <div v-if="form.images.length" class="form-row">
            <label class="form-label" for="images"></label>
            <div class="form-field">
                <p>Still Image Files:</p>
                <div class="thumbnail-list" v-if="form.images.length">
                    <div
                    class="thumb"
                    v-for="(file, index) in form.images"
                    :key="file.name"
                    @click="removeImage(index)"
                    title="Click to remove"
                    >
                    <img :src="blobUrl(file)" :alt="file.name" />
                </div>
            </div>
        </div>
    </div>
    
    <div class="form-row">
        <label class="form-label" for="description">Description</label>
        <div class="form-field">
            <textarea id="description" v-model="form.description" rows="3"></textarea>
        </div>
    </div>
    
    <div class="form-row">
        <label class="form-label" for="creator">Creator</label>
        <div class="form-field">
            <input id="creator" v-model="form.creator" type="text" />
        </div>
    </div>
    
    <div class="form-row">
        <label class="form-label" for="date">Date</label>
        <div class="form-field">
            <input id="date" v-model="form.date" type="text" />
        </div>
    </div>
    
    <div class="form-row">
        <label class="form-label" for="copyright">Copyright</label>
        <div class="form-field">
            <input id="copyright" v-model="form.copyright" type="text" />
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