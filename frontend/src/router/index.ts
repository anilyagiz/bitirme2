import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('../pages/Login.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/staff/tasks',
      name: 'StaffTasks',
      component: () => import('../pages/staff/Tasks.vue'),
      meta: { requiresAuth: true, role: 'staff' }
    },
    {
      path: '/staff/tasks/:id',
      name: 'StaffTaskDetail',
      component: () => import('../pages/staff/TaskDetail.vue'),
      meta: { requiresAuth: true, role: 'staff' }
    },
    {
      path: '/supervisor/reviews',
      name: 'SupervisorReviews',
      component: () => import('../pages/supervisor/Reviews.vue'),
      meta: { requiresAuth: true, role: 'supervisor' }
    },
    {
      path: '/supervisor/reviews/:id',
      name: 'SupervisorReviewDetail',
      component: () => import('../pages/supervisor/ReviewDetail.vue'),
      meta: { requiresAuth: true, role: 'supervisor' }
    },
    {
      path: '/admin/dashboard',
      name: 'AdminDashboard',
      component: () => import('../pages/admin/Dashboard.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/',
      redirect: '/login'
    }
  ]
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.role && authStore.user?.role !== to.meta.role) {
    // Redirect based on user role
    if (authStore.user?.role === 'admin') {
      next('/admin/dashboard')
    } else if (authStore.user?.role === 'staff') {
      next('/staff/tasks')
    } else if (authStore.user?.role === 'supervisor') {
      next('/supervisor/reviews')
    } else {
      next('/login')
    }
  } else {
    next()
  }
})

export default router
