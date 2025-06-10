import { createWebHistory, createRouter } from 'vue-router'

import List from './components/List.vue'
import ArtifactView from './views/ArtifactView.vue'
import UploadView from './views/UploadView.vue'

const routes = [
    { path: '/', component: List },
    { path: '/artifact/:id', name: 'artifact', component: ArtifactView, props: true },
    { path: '/upload', name: 'upload', component: UploadView },
    
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router