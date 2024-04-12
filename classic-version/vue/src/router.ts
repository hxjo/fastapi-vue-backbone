import { createWebHistory, createRouter } from 'vue-router'
import { useCurrentUserStore } from '@/stores/currentUser'
import { storeToRefs } from 'pinia'

const routes = [
  { path: '/', component: () => import('./Pages/HomeView.vue') },
  { path: '/app', component: () => import('./Pages/AppView.vue') },
  { path: '/auth/login', component: () => import('./Pages/auth/LoginView.vue') },
  {
    path: '/auth/logout',
    redirect: () => {
      useCurrentUserStore().logOut()
      return { path: '/auth/login' }
    }
  },
  { path: '/auth/signup', component: () => import('./Pages/auth/SignupView.vue') },
  {
    path: '/auth/recover-password',
    component: () => import('./Pages/auth/RecoverPasswordView.vue')
  },
  {
    path: '/auth/reset-password',
    component: () => import('./Pages/auth/ResetPasswordView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const authRoutes = ['/auth/login', '/auth/signup', '/auth/recover-password', '/auth/reset-password']
const publicRoutes = ['/', ...authRoutes]

router.beforeEach(async (to) => {
  const currentUserStore = useCurrentUserStore()
  const { isLoggedIn } = storeToRefs(currentUserStore)
  if (!isLoggedIn.value) {
    await currentUserStore.autoLogin()
  }
  if (!isLoggedIn.value && !publicRoutes.includes(to.path)) {
    return { path: '/auth/login' }
  }

  if (authRoutes.includes(to.path) && isLoggedIn.value) {
    return { path: '/' }
  }
})

export default router
