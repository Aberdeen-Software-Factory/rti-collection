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
    images.value.splice(index, 1)
}

function removeRTI(index) {
    webrtis.value.splice(index, 1);
}

function removePtm(index) {
    ptms.value.splice(index, 1);
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
    <div class="self-baseline">
    <label class="btn btn-accent self-baseline w-full">
        Add Files
        <input
            id="images"
            type="file"
            class="hidden"
            accept=".jpg, .zip, .ptm"
            multiple
            @change="onImageSelected" />
    </label>
        <label class="label self-baseline">Supported file formats: .ptm, .jpg, .zip</label>

    <!-- <div class="form-row">
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
    </div> -->
    
    <div v-if="ptms.length" class="form-row">
        <div class="form-field">
            <label class="label text-sm py-2">Polynomial Texture Map (.ptm) Files:</label>
            <div class="flex flex-col gap-2" v-if="ptms.length">
                <div
                    v-for="(file, index) in ptms"
                    class="card bg-base-100 border border-base-100 flex flex-row p-2 items-center"
                    :key="file.name"
                    title="Click to remove"
                >
                    <p class="text-sm flex-grow align-middle">{{ file.name }}</p>
                    <!-- <img :src="blobUrl(file)" :alt="file.name" /> -->
                    <button
                        class="btn btn-accent btn-sm btn-square"
                        @click="() => removePtm(index)"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                        </svg>
                    </button>
            </div>
        </div>
    </div>
</div>

<!-- RTI upload -->
<div v-if="webrtis.length" class="form-row">
    <div class="form-field">
        <!-- <input id="RTIs" type="file" multiple @change="onRTISelected"/> -->
        <label class="label text-sm py-2">Relight Web Format Files:</label>
        <div class="grid grid-cols-3 gap-2" v-if="webrtis.length">
            <div
                v-for="(file, index) in webrtis"
                :key="file.name"
                class="relative card card-bordered aspect-square object-cover bg-base-100 overflow-hidden border border-base-200"
                title="Click to remove"
            >
                <ZipPreview :zipFile="file" :filename="'plane_0.jpg'" class="h-full w-full object-cover"/>
                <button
                    class="btn btn-accent btn-sm btn-square absolute top-2 right-2 z-10"
                    @click="() => removeRTI(index)"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>
        </div>
    </div>
</div>

<div v-if="images.length" class="form-row">
    <label class="form-label" for="images"></label>
    <div class="form-field">
        <label class="label text-sm py-2">Still Image Files:</label>
        <div class="grid grid-cols-3 gap-4" v-if="images.length">
            <div
                class="relative card card-bordered aspect-square object-cover bg-base-100 overflow-hidden border border-base-200"
                v-for="(file, index) in images"
                :key="file.name"
                title="Click to remove"
            >
            <img :src="blobUrl(file)" :alt="file.name" />
            <button
                class="btn btn-accent btn-sm btn-square absolute top-2 right-2 z-10"
                @click="() => removeImage(index)"
            >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                </svg>
            </button>
        </div>
    </div>
</div>
</div>
</div>
</template>

<style scoped>
</style>