import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store/store.js'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

// component: has import for the components because of route level code-splitting
// this generates a separate chunk for each route which is lazy-loaded when the route is visited.

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
      meta: { title: 'Home | UTSC CourseTree', access: 0 }
    },
    {
      path: '/courses',
      name: 'courses',
      component: () => import('../views/Courses.vue'),
      meta: { title: 'Directory | UTSC CourseTree', access: 0 }
    },
    {
      path: '/treeview',
      name: 'treeview',
      component: () => import('../views/TreeView.vue'),
      meta: { title: 'TreeView | UTSC CourseTree', access: 0 }
    },
    {
      path: '/information',
      name: 'information',
      component: () => import('../views/Information.vue'),
      meta: { title: 'Links & Info | UTSC CourseTree', access: 0 }
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/Admin.vue'),
      meta: { title: 'ADMIN | UTSC CourseTree', access: 3 }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/Dashboard.vue'),
      meta: { title: 'Dashboard | UTSC CourseTree', access: 1 }
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutUs.vue'),
      meta: { title: 'About Us | UTSC CourseTree', access: 0 }
    },
    {
      path: '/feedback',
      name: 'feedback',
      component: () => import('../views/Feedback.vue'),
      meta: { title: 'Feedback & Updates | UTSC CourseTree', access: 0 }
    },
    {
      path: '*',
      redirect: '/'
    }
  ]
})

router.beforeEach((to, from, next) => {
  // First load the page lock data from db then determine
  store.dispatch('loadLocks').then(() => {
    // If the user has access to the page proceed to check locks otherwise ignore
    if (to.meta.access <= store.state.user.access) {
      if (to.fullPath === '/courses' && !store.state.coursePage) {
        next('/')
      } else if (to.fullPath === '/treeview' && !store.state.treeViewPage) {
        next('/')
      } else if (to.fullPath === '/information' && !store.state.infoPage) {
        next('/')
      } else {
        next()
      }
    } else {
      alert('Unauthorized!')
    }
  })
})

// Change the tab title based on what page we are on after navigating to it
router.afterEach((to, from) => {
  document.title = to.meta.title
})

export default router
