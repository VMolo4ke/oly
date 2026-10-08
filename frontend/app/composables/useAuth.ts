import type { TokenResponse, User } from '~/types'

export function useAuth() {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase

  const token = useCookie<string | null>('access_token', {
    maxAge: 60 * 60 * 24 * 7,
    sameSite: 'lax',
    default: () => null
  })
  const user = useState<User | null>('auth-user', () => null)

  const isAuthenticated = computed(() => !!token.value)

  async function fetchUser() {
    if (!token.value) {
      user.value = null
      return null
    }
    try {
      user.value = await $fetch<User>('/users/me', {
        baseURL,
        headers: { Authorization: `Bearer ${token.value}` }
      })
    } catch {
      logout()
    }
    return user.value
  }

  async function login(email: string, password: string) {
    const data = await $fetch<TokenResponse>('/auth/login', {
      baseURL,
      method: 'POST',
      body: { email, password }
    })
    token.value = data.access_token
    await fetchUser()
  }

  async function register(email: string, password: string) {
    await $fetch<User>('/auth/register', {
      baseURL,
      method: 'POST',
      body: { email, password }
    })
    // После успешной регистрации сразу логиним пользователя
    await login(email, password)
  }

  function logout() {
    token.value = null
    user.value = null
  }

  return { token, user, isAuthenticated, fetchUser, login, register, logout }
}
