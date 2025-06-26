<script setup>
import ArtifactCard from './ArtifactCard.vue';
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useArtifacts } from '@/composables/useArtifacts';
import LoadingHero from '@/components/display/LoadingHero.vue';

const route = useRoute()
const router = useRouter()

const pageSizeOptions = [25, 50, 100]
const selectedPage = ref(parseInt(route.query.page) || 1)
const selectedPageSize = ref(parseInt(route.query.page_size) || pageSizeOptions[0])

const { artifacts, currentPage, totalPages, error, loading } = useArtifacts(selectedPage, selectedPageSize)

watch(
  [currentPage, selectedPageSize],
  ([newPage, newPageSize]) => {
    router.replace({
      query: {
        ...route.query,
        page: newPage,
        page_size: newPageSize
      }
    })
  },
  // { immediate: true }
)
</script>

<template>
  <template v-if="loading">
    <LoadingHero />
  </template>

  <div v-else-if="artifacts.length > 0" class="flex-grow bg-base-200">
    <div class="flex flex-col max-w-340 mx-auto">
      <div class="p-4 md:p-8 grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
        <RouterLink v-for="(artifact, index) in artifacts" :to="`/artifacts/${artifact.id}`">
          <ArtifactCard :key="index" :artifact="artifact" />
        </RouterLink>
      </div>

      <div class="flex justify-end items-center gap-4 p-4 md:p-8">
        <div class="join">
          <button class="join-item btn btn-outline pointer-events-none select-none" tabindex="-1">
            Results per page
          </button>
          <select v-model="selectedPageSize"
            class="join-item select border-[var(--border)] border-base-content bg-transparent text-base-content font-medium cursor-pointer w-fit">
            <option v-for="size in pageSizeOptions" :key="size" :value="size">
              {{ size }}
            </option>
            <option v-if="!pageSizeOptions.includes(selectedPageSize)" :key="selectedPageSize"
              :value="selectedPageSize">
              {{ selectedPageSize }}</option>
          </select>
        </div>

        <div class="join">
          <button v-if="currentPage > 1" class="join-item btn btn-square btn-outline"
            :class="{ 'btn-disabled': currentPage <= 1 }" @click="selectedPage = currentPage - 1">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="size-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
            </svg>
          </button>

          <button class="join-item btn btn-outline pointer-events-none select-none">Page {{ currentPage }}</button>

          <button v-if="currentPage < totalPages" class="join-item btn btn-square btn-outline"
            :class="{ 'btn-disabled': currentPage >= totalPages }" @click="selectedPage = currentPage + 1">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="size-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
            </svg>

          </button>
        </div>
      </div>
    </div>
  </div>

  <div v-else-if="!loading" class="hero bg-base-200 flex-grow">
    <div class="hero-content text-center">
      <div class="max-w-md">
        <h1 className="text-5xl font-bold">Empty collection</h1>
        <p className="py-6">
          There are no artifacts in this collection. Start by uploading some if you are authorised.
        </p>
        <RouterLink to="/upload" className="btn btn-primary">Upload Artifact</RouterLink>
      </div>
    </div>
  </div>
</template>
