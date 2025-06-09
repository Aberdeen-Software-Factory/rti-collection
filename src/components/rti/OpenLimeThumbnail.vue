<script setup>
const props = defineProps(['url'])
import { ref, onMounted, watch } from 'vue'

const limeContainer = ref()
let lime = null

async function initViewer(url) {
    try {

        // Clean up previous viewer if necessary
        if (lime) {
            lime.destroy?.()
        }
        
        let layout = 'image'
        let normals = false
        // Create new viewer
        lime = new OpenLIME.Viewer(limeContainer.value, {
            background:'black',
        })
        
        const layer = new OpenLIME.Layer({
            type: 'rti',
            url: url + '/info.json',
            layout: 'image',
            normals: false,
        })
        
        lime.addLayer('rti', layer); 

        // OpenLIME.Skin.setUrl('openlime/skin.svg');
        // let ui = new OpenLIME.UIBasic(viewerInstance, { skin: 'openlime/skin.svg', showLightDirections: true });
        // ui.actions.light.active = true;
        // ui.actions.layers.display = true;
        // lime.camera.maxFixedZoom = 1;
        
    } catch (err) {
        console.error('Failed to initialize RelightViewer:', err)
    }
}

onMounted(() => {
    initViewer(props.url)
})

// Watch for url prop changes
watch(() => props.url, (newUrl) => {
    if (newUrl) {
        initViewer(newUrl)
    }
})
</script>

<template>
  <div ref="limeContainer" class="openlime thumbnail"></div>
</template>

<style scoped>
.openlime {
  width: 100%;
  height: 100%;
  padding: 0;
  margin: 0;
  overflow: hidden;
}

.thumbnail {
    flex-shrink: 0;
    width: 100px;
    height: 100px;
    object-fit: cover;
    border: 2px solid transparent;
    border-radius: 8px;
    /* overflow: hidden; */
    cursor: pointer;
    transition: transform 0.2s;
}

.thumbnail:hover {
    transform: scale(1.05);
}

.thumbnail.selected {
    border-color: #007BFF;
}
</style>