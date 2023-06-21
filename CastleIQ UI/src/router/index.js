import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import TestVue from '../views/TestView.vue'
import LogInView from '../views/LogInView.vue'
import UsersView from '../views/UsersView.vue'
import DevicesView from '../views/DevicesView.vue'
import AutomationsView from '../views/AutomationsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/test',
      name: 'test',
      component: TestVue
    },
    {
      path: '/login',
      name: 'login',
      component: LogInView
    },
    // {
    //   path: '/users',
    //   name: 'users',
    //   component: UsersView
    // },
    {
      path: '/devices',
      name: 'devices',
      component: DevicesView
    },
    {
      path: '/automations',
      name: 'automations',
      component: AutomationsView
    }
  ]
})

export default router
