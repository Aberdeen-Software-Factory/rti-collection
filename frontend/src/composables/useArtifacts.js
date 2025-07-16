import ArtifactPreview from "@/models/ArtifactPreview"
import { computed, toValue } from "vue"
import { useFetch } from "@/composables/useFetch"

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

/**
 * Composable to fetch paginated artifact previews.
 *
 * @param {number|import('vue').Ref<number>} [page=1] - The current page number or a ref.
 * @param {number|import('vue').Ref<number>} [pageSize=4] - Number of items per page or a ref.
 * @returns {{
 *   artifacts: import('vue').ComputedRef<ArtifactPreview[]>,
 *   currentPage: import('vue').ComputedRef<number>,
 *   totalPages: import('vue').ComputedRef<number>,
 *   error: import('vue').Ref<any>,
 *   loading: import('vue').Ref<boolean>
 * }}
 */
export function useArtifacts(page = 1, pageSize = 50) {

    const url = computed(() => {
        const params = new URLSearchParams({
            page: toValue(page),
            page_size: toValue(pageSize),
        })
        return `/api/artifacts?${params.toString()}`
    })

    const { data, error, loading } = useFetch(url)

    const artifacts = computed(() => 
        (data?.value?.artifacts ?? []).map(data => new ArtifactPreview(data))
    )
    const currentPage = computed(() => data?.value?.page ?? 1)
    const totalPages = computed(() => data?.value?.pages ?? 1)

    return { artifacts, currentPage, totalPages, error, loading }
}