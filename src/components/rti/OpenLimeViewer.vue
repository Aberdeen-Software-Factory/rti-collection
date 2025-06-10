<!-- https://vcg.isti.cnr.it/vcgtools/relight// -->
<script setup>
const props = defineProps(['url']);
import { ref, onMounted, watch } from 'vue';

let limeElement = ref();

function initViewer(url) {
	limeElement.value.replaceChildren();

	if (url.endsWith('info.json')) {
		initRTI('.openlime', url);
	} else if (url.endsWith('.jpg')) {
		initJPG('.openlime', url);
	}
}

onMounted(() => {
	initViewer(props.url)
})

watch(() => props.url, (newUrl) => {
	if (newUrl) {
		initViewer(newUrl)
	}
})

function initRTI(viewer, path) {
	// let layout = await autodetect(path);
	// let normals = await autodetectNormals(layout, path);
	let layout = 'image';
	let normals = false;
	
	var lime = new OpenLIME.Viewer(viewer, {
		background: 'black'
	});
	
	let layer = new OpenLIME.Layer({
		type:'rti',
		url: path,
		layout: layout, 
		normals: normals
	});
	
	lime.canvas.addLayer('RTI', layer); 
	OpenLIME.Skin.setUrl(new URL('openlime/skin.svg', window.location.origin).toString());
	// OpenLIME.Skin.setUrl('openlime/skin.svg');

	let ui = new OpenLIME.UIBasic(lime, {
		// skin: 'skin.svg',
		showLightDirections: false
	});
	// ui.actions.light.active = true;
	ui.toggleLightController(true);
	
	// ui.actions.layers.display = true;
	lime.camera.maxFixedZoom = 1;
	window.lime = lime;
	
	return [lime, ui]
}

function initJPG(viewer, path) {
	let layout = 'image';
	let normals = false;
	
	var lime = new OpenLIME.Viewer(viewer, {
		background: 'black'
	});
	
	let layer = new OpenLIME.LayerImage({
		id: 'base-image',
		layout: 'image',
		url: path,
	});
	
	lime.canvas.addLayer('JPG', layer);
	OpenLIME.Skin.setUrl(new URL('openlime/skin.svg', window.location.origin).toString());

	let ui = new OpenLIME.UIBasic(lime);
	ui.actions.light.display = false;
	ui.actions.layers.display = false;
	
	// ui.actions.layers.display = true;
	lime.camera.maxFixedZoom = 1;
	window.lime = lime;
	
	return [lime, ui]
}
</script>

<template>
	<div ref="limeElement" class="openlime"></div>
</template>

<style scoped>
.openlime {
	width: 100%;
	height: 400px;
	max-height: 400px;
	padding: 0;
	margin: 0;
}
</style>
