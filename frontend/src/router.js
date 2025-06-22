import { createWebHistory, createRouter } from 'vue-router'

import CollectionView from './views/CollectionView.vue'
import ArtifactView from './views/ArtifactView.vue'
import ArtifactEditView from './views/ArtifactEditView.vue'
import UploadView from './views/UploadView.vue'

const routes = [
    { path: '/', component: CollectionView },
    { path: '/artifacts/:id', name: 'artifact', component: ArtifactView, props: true },
    { path: '/artifacts/:id/edit', name: 'artifact-edit', component: ArtifactEditView, props: true },
    { path: '/upload', name: 'upload', component: UploadView },
    
]

const REPO_NAME = import.meta.env.VITE_REPO_NAME

const router = createRouter({
    history: createWebHistory(REPO_NAME),
    routes,
    scrollBehavior(to, from, savedPosition) {
        // always scroll to top on route change
        return { top: 0 }
    },
})

export default router