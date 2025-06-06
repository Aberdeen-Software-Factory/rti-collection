<script setup>
import { onMounted, watch } from 'vue'

const props = defineProps(['url'])

function loadScript(src) {
  return new Promise((resolve, reject) => {
    if (document.querySelector(`script[src="${src}"]`)) {
      return resolve()
    }

    const script = document.createElement('script')
    script.src = src
    script.async = true
    script.onload = resolve
    script.onerror = reject
    document.head.appendChild(script)
  })
}

function loadStyle(href) {
  if (!document.querySelector(`link[href="${href}"]`)) {
    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.href = href
    document.head.appendChild(link)
  }
}


let viewerInstance = null

async function initViewer(url) {
  try {
    // Only load scripts/styles once
    loadStyle('relight-viewer/css/relight.css')
    await loadScript('relight-viewer/hammer.min.js')
    await loadScript('relight-viewer/relight-viewer.min.js')

    // Clean up previous viewer if necessary
    if (viewerInstance) {
      viewerInstance.destroy?.()
      viewerInstance = null
    }

    // Create new viewer
    viewerInstance = new window.RelightViewer('.relight', {
      url,
      layout: 'image',
    })
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
  <div class="relight"></div>
</template>

<style scoped>
.relight {
  width: 100%;
  height: 100%;
  padding: 0;
  margin: 0;
}
</style>
