import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type { UserOut } from '@/api'
import { useCookies } from '@vueuse/integrations/useCookies'
import { OpenAPI, UsersService } from '@/api'

export const useCurrentUserStore = defineStore('currentUser', () => {
  const cookies = useCookies()

  const _user = ref<UserOut | null>(null)
  const isLoggedIn = computed(() => !!_user.value)
  function setUser(newUser: UserOut) {
    _user.value = newUser
  }

  async function autoLogin() {
    const token = cookies.get('access_token')
    if (token) {
      OpenAPI.TOKEN = token
      try {
        const user = await UsersService.getUserMeApiV1UsersMeGet()
        setUser(user)
      } catch (error) {
        logOut()
      }
    }
  }

  function logOut() {
    _user.value = null
    cookies.remove('access_token')
  }

  function getDefaultUserOut(): UserOut {
    console.error('getDefaultUserOut called')
    return {
      email: 'default@default.com',
      username: 'default',
      id: 0,
      is_active: false
    }
  }
  const user = computed<UserOut>(() => _user.value ?? getDefaultUserOut())

  return { user, isLoggedIn, setUser, autoLogin, logOut }
})
