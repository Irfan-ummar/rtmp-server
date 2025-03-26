import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import CameraAddView from '../views/CameraAddView.vue'
import CameraDetailView from '../views/CameraDetailView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: DashboardView
  },
  {
    path: '/cameras/add',
    name: 'camera-add',
    component: CameraAddView
  },
  {
    path: '/cameras/:id',
    name: 'camera-detail',
    component: CameraDetailView,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router 