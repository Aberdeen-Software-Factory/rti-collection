<script setup>
import { ref, onMounted } from 'vue';
import JSZip from "jszip";

const props = defineProps(['zipFile', 'filename']);
const url = ref('')

async function getUrlForFileInZip(zipFile, filename) {
  const zip = await JSZip.loadAsync(zipFile); // Load the ZIP contents

// Get all files in the ZIP
  const filenames = Object.keys(zip.files);

  // Find the first file that ends with the given extension and is not a directory
  const match = filenames.find(name => 
    name.endsWith(filename) && !zip.files[name].dir
  );

  if (!match) {
    throw new Error(`No file ending with "${extension}" found in ZIP.`);
  }

  const file = zip.files[match];
    console.log(file)
  const blob = await file.async("blob"); // Extract the file as a Blob
  const url = URL.createObjectURL(blob); // Create a temporary object URL
  console.log(url)
  return url;
}

onMounted(async () => {
    url.value = await getUrlForFileInZip(props.zipFile, props.filename)
})
</script>

<template>
    <img :src="url"/>
</template>