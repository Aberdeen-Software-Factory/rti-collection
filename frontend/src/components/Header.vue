<script setup>
import ThemePicker from './ThemePicker.vue';

/**
* @typedef {Object} Segment
* @property {string} label
* @property {string} dest
*/

const props = defineProps({
    segments: {
        type: Array,
        required: true,
    },
    title: String,
});
</script>

<template>
    <div class="w-full bg-base-300 text-base-content">
        <div class="flex flex-wrap max-w-340 mx-auto md:p-8 gap-2 items-center">
            <div class="flex-grow-1">
                <div>
                    <div class="breadcrumbs text-sm">
                        <ul>
                            <li v-for="(segment) in segments">
                                <RouterLink
                                v-if="segment.dest"
                                :to="segment.dest"
                                >{{ segment.label }}</RouterLink>
                                <template v-else>
                                    {{ segment.label }}
                                </template>
                            </li>
                        </ul>
                    </div>
                </div>
                <div>
                    <h1 class="text-4xl md:text-6xl">{{ title }}</h1>
                </div>

                
            </div>
            <div class="flex gap-2 my-2">
                <ThemePicker/>
                <RouterLink to="/upload" class="btn">Upload Artifact</RouterLink>
            </div>
        </div>
    </div>
<!-- <div class="navbar bg-base-100 text-base-content ">
    <div class="flex-1">
        <p class="font-bold px-4 text-xl">Relightable Collection</p>
    </div>
    <div>
        <RouterLink to="/upload" class="btn btn-ghost">Upload</RouterLink>
    </div>
</div> -->
</template>
