import { computed, toValue } from 'vue'
import { useFetch } from './useFetch' // or wherever your composable is
import { Artifact } from '@/model/artifact'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

/**
 * Fetch an artifact JSON from given URL
 * @param {string | Ref<string>} id
 * @returns {{ artifact: import('vue').Ref<Artifact>, error: import('vue').Ref<Error | null> }}
 */
export function useArtifact(id) {
    const url = new URL(`artifacts/${toValue(id)}`, API_BASE_URL).toString()
    const { data, error } = useFetch(url)
    
    const artifact = computed(() => {
        if (!data.value || !data.value.artifact) return null
        return new Artifact(data.value.artifact)
    })

    return { artifact, error }
}