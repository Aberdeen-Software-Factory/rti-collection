<script setup>
import JSZip from "jszip";
import ZipPreview from '../ZipPreview.vue'

const images = defineModel('images');
const webrtis = defineModel('webrtis');
const ptms = defineModel('ptms');

const prop = defineProps({
    label: String,
});

function getFileExtension(file) {
    const parts = file.name.split('.');
    return parts.length > 1 ? parts.pop().toLowerCase() : '';
}

function onImageSelected(event) {
    const files = Array.from(event.target.files)
    console.log(files)
    for (const file of files) {
        console.log("here")
        switch (getFileExtension(file)) {
            case "jpg":
                images.value.push(file);
                break;
            case "zip":
                webrtis.value.push(file);
                break;
            case "ptm":
                ptms.value.push(file);
                break;
            default:
                console.log(`Unsupported file uploaded: ${file.name}`)
        }
    }

    event.target.value = null
}

function removeImage(index) {
    images.splice(index, 1)
}

function removeRTI(index) {
    webrtis.splice(index, 1);
}

function removePtm(index) {
    ptms.splice(index, 1);
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
    <div class="form-row">
        <label class="form-label" for="images">{{ label }}</label>
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
    
    <div v-if="ptms.length" class="form-row">
        <label class="form-label" for="images"></label>
        <div class="form-field">
            <h4>Polynomial Texture Map (.ptm) Files:</h4>
            <div class="thumbnail-list" v-if="ptms.length">
                <div
                class="thumb"
                v-for="(file, index) in ptms"
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
<div v-if="webrtis.length" class="form-row">
    <label class="form-label" for="RTIs"></label>
    <div class="form-field">
        <!-- <input id="RTIs" type="file" multiple @change="onRTISelected"/> -->
        <h4>Relight Web Format Files:</h4>
        <div class="thumbnail-list" v-if="webrtis.length">
            <div class="thumb" v-for="(files, index) in webrtis" :key="index" @click="removeRTI(index)" title="Click to remove">
                <p>{{ files.length }} files</p>
                <!-- <img :src="blobUrl(getPlane0(files))" /> -->
                <ZipPreview :zipFile="files" :filename="'plane_0.jpg'"/>
            </div>
        </div>
    </div>
</div>

<div v-if="images.length" class="form-row">
    <label class="form-label" for="images"></label>
    <div class="form-field">
        <p>Still Image Files:</p>
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
</div>
</div>
</template>

<style scoped>
</style>