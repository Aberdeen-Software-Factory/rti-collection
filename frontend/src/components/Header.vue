<script setup>
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
    <div class="max-w-340 mx-auto w-full md:p-8 bg-base-300 text-base-content">
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
            <h1 class="text-7xl">{{ title }}</h1>
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
