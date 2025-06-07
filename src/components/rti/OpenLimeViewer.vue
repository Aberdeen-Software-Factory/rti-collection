<!-- https://vcg.isti.cnr.it/vcgtools/relight// -->
<script setup>
const props = defineProps(['url'])
import { onMounted, watch } from 'vue'
import { loadScript, loadStyle } from '../utils.js'

console.log(props.url)
let viewerInstance = null

async function autodetect(url) {
	let response = await fetch(url + '/plane_0.tzi');
	if(response.status == 200)
		return "tarzoom";

	response = await fetch(url + '/plane_0.dzi');
	if(response.status == 200)
		return "deepzoom";

        response = await fetch(url + '/planes.tzi');
        if(response.status == 200)
                return "itarzoom";

	response = await fetch(url + '/plane_0.jpg');
	if(response.status == 200)
                return "image";

	alert("Could not detect an RTI here");
	return "";
}

async function autodetectNormals(layout) {
    //TODO need work response reads 200 even if resource doesnt exist (same in function above)
	if(layout == 'tarzoom') {
		let response = await fetch('normals.tzi');
		if(response.status == 200)
			return true;
	}
	if(layout == 'deepzoom') {
		let response = await fetch('normals.dzi');
		if(response.status == 200)
			return true;
	}
	if(layout == 'image') {
		let response = await fetch('normals.jpg');
        console.log(response)
		if(response.status == 200)
			return true;
	}

	return false;
}

async function initViewer(url) {
  try {
    // Only load scripts/styles once
    loadStyle('openlime/skin.css')
    await loadScript('openlime/openlime.min.js')

    // Clean up previous viewer if necessary
    if (viewerInstance) {
      viewerInstance.destroy?.()
      viewerInstance = null
    }

    let layout = 'image'
	let normals = false
    // Create new viewer
    viewerInstance = new OpenLIME.Viewer('.openlime', { background:'black' });

    let layer = new OpenLIME.Layer({
        type:'rti',
		url: url + '/info.json',
		layout: layout, 
		normals: normals,
	})

	viewerInstance.addLayer('RTI', layer); 
	OpenLIME.Skin.setUrl('openlime/skin.svg');
	let ui = new OpenLIME.UIBasic(viewerInstance, { skin: 'openlime/skin.svg', showLightDirections: true });
	ui.actions.light.active = true;
	ui.actions.layers.display = true;
	viewerInstance.camera.maxFixedZoom = 1;

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
  <div class="openlime"></div>
</template>

<style scoped>
.openlime {
  width: 100%;
  height: 100%;
  padding: 0;
  margin: 0;
}
</style>
