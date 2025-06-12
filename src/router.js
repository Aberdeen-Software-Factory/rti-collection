import { createWebHistory, createRouter } from 'vue-router'

import Collection from './components/Collection.vue'
import ArtifactView from './views/ArtifactView.vue'
import UploadView from './views/UploadView.vue'

const routes = [
    { path: '/', component: Collection },
    { path: '/artifact/:id', name: 'artifact', component: ArtifactView, props: true },
    { path: '/upload', name: 'upload', component: UploadView },
    
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router