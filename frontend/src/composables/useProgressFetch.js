import { ref, toValue, computed } from 'vue'

export function useProgressFetch(url) {
    const data = ref(null)
    const error = ref(null)
    const uploadProgress = ref(0)
    const downloadProgress = ref(0)
    const totalProgress = computed(() => {
        return (uploadProgress.value + downloadProgress.value) / 2
    })
    const isLoading = ref(false);
        
    const progressFetch = ({ method, headers = {}, body }) => {
        // reset state before fetching..
        data.value = null;
        error.value = null;
        uploadProgress.value = 0;
        downloadProgress.value = 0;
        isLoading.value = true;
        
        const xhr = new XMLHttpRequest()
        
        xhr.upload.onprogress = (event) => {
            if (event.lengthComputable) {
                console.log('Upload progress:', event.loaded, '/', event.total)
                uploadProgress.value = event.loaded / event.total
            }
        }
        
        xhr.onprogress = (event) => {
            if (event.lengthComputable) {
                downloadProgress.value = event.loaded / event.total
            }
        }
        
        xhr.onload = () => {
            isLoading.value = false;
            if (xhr.status >= 200 && xhr.status < 300) {
                try {
                    data.value = JSON.parse(xhr.responseText)
                } catch (e) {
                    data.value = xhr.responseText
                }
            } else {
                error.value = new Error(`Upload failed with status ${xhr.status}`)
            }
        }
        
        xhr.onerror = () => {
            isLoading.value = false;
            error.value = new Error('Network error during upload')
        }
        
        xhr.open(toValue(method), toValue(url))
        for (const [name, value] of Object.entries(toValue(headers))) {
            xhr.setRequestHeader(name, value)
        }
        xhr.send(toValue(body))
    }
    
    return {
        data,
        error,
        uploadProgress,
        downloadProgress,
        totalProgress,
        isLoading,
        progressFetch,
    }
}
