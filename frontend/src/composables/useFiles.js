import { ref, watch, toValue } from "vue"

/**
 * @typedef {Object} FileFetchResult
 * @property {string} url - The URL that was fetched.
 * @property {File|null} file - The successfully fetched file, or null if there was an error.
 * @property {string|null} error - The error message if the fetch failed, otherwise null.
 */

export function useFiles(urls) {
    /**
     * @type {import('vue').Ref<Record<string, FileFetchResult>>}
     */
    const results = ref({})
    const loading = ref(false)

    const fetchFiles = async () => {
        loading.value = true
        results.value = {}

        await Promise.all(
            toValue(urls).map(async (url) => {
                try {
                    const res = await fetch(url)

                    if (!res.ok) {
                        results.value = {
                            ...results.value,
                            [url]: {
                                file: null,
                                error: `HTTP ${res.status} - ${res.statusText}`,
                            }
                        }
                        return
                    }

                    const blob = await res.blob()
                    const filename = url.split('/').pop() || 'downloaded_file'

                    results.value = {
                        ...results.value,
                        [url]: {
                            file: new File([blob], filename, { type: blob.type }),
                            error: null,
                        }
                    }
                } catch (err) {
                    results.value = {
                        ...results.value,
                        [url]: {
                            file: null,
                            error: err instanceof Error ? err.message : String(err),
                        }
                    }
                }
            })
        )

        loading.value = false
    }


    watch(() => {
        fetchFiles()
    })

    return { results, loading }
}
