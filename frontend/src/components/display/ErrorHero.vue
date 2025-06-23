<script setup>
defineProps({
    error: Error,
})
</script>

<template>
    <div class="hero bg-base-200 flex-grow">
        <div class="hero-content text-center">
            <div class="max-w-md">
                <h1 class="text-5xl font-bold">Error</h1>
                <p class="py-6">
                    {{ error }}
                </p>
                <RouterLink to="/" class="btn btn-primary w-40">Back Home</RouterLink>
            </div>
        </div>
    </div>
</template>