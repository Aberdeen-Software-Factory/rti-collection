import { ref, watchEffect, toValue } from 'vue'

export function useFetch(url) {
    const data = ref(null)
    const error = ref(null)
    const loading = ref(false)
    
    const fetchData = () => {
        // reset state before fetching..
        data.value = null
        error.value = null
        loading.value = true
        
        fetch(toValue(url))
            .then((res) => res.json())
            .then((json) => (data.value = json))
            .catch((err) => (error.value = err))
            .finally(() => (loading.value = false))
    }
    
    watchEffect(() => {
        fetchData();
    })
    
    return { data, error, loading }
}
