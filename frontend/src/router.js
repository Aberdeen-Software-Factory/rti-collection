import { createWebHistory, createRouter } from 'vue-router'

import CollectionView from './views/CollectionView.vue'
import ArtifactView from './views/ArtifactView.vue'
import UploadView from './views/UploadView.vue'

const routes = [
    { path: '/', component: CollectionView },
    { path: '/artifacts/:id', name: 'artifact', component: ArtifactView, props: true },
    { path: '/upload', name: 'upload', component: UploadView },
    
]

const REPO_NAME = import.meta.env.VITE_REPO_NAME

const router = createRouter({
    history: createWebHistory(REPO_NAME),
    routes,
})

export default router