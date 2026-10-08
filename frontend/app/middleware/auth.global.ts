export default defineNuxtRouteMiddleware(async (to) => {
  const { isAuthenticated, user, fetchUser } = useAuth()
  const isAuthPage = to.path.startsWith('/auth')

  if (!isAuthenticated.value) {
    return isAuthPage ? undefined : navigateTo('/auth/login')
  }

  // Подгружаем профиль, если токен есть, а пользователя ещё нет
  if (!user.value) {
    await fetchUser()
  }

  if (!isAuthenticated.value) {
    return isAuthPage ? undefined : navigateTo('/auth/login')
  }
  if (isAuthPage) {
    return navigateTo('/')
  }
})
