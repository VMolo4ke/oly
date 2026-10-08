<template>
  <div class="auth">
    <form class="auth__card" @submit.prevent="onSubmit">
      <h1 class="auth__title">{{ isLogin ? 'Вход' : 'Регистрация' }}</h1>

      <CommonInput
        v-model="email"
        label="Email"
        type="email"
        placeholder="you@example.com"
        autocomplete="email"
        required
      />
      <CommonInput
        v-model="password"
        label="Пароль"
        type="password"
        placeholder="Минимум 8 символов"
        :autocomplete="isLogin ? 'current-password' : 'new-password'"
        :minlength="isLogin ? undefined : 8"
        :maxlength="72"
        required
      />
      <CommonInput
        v-if="!isLogin"
        v-model="confirm"
        label="Повторите пароль"
        type="password"
        autocomplete="new-password"
        required
      />

      <p v-if="error" class="auth__error">{{ error }}</p>

      <CommonButton type="submit" :loading="pending">
        {{ isLogin ? 'Войти' : 'Создать аккаунт' }}
      </CommonButton>

      <p class="auth__switch">
        <template v-if="isLogin">
          Нет аккаунта?
          <NuxtLink to="/auth/register">Зарегистрироваться</NuxtLink>
        </template>
        <template v-else>
          Уже есть аккаунт?
          <NuxtLink to="/auth/login">Войти</NuxtLink>
        </template>
      </p>
    </form>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  mode: 'login' | 'register'
}>()

const { login, register } = useAuth()

const isLogin = computed(() => props.mode === 'login')

const email = ref('')
const password = ref('')
const confirm = ref('')
const error = ref('')
const pending = ref(false)

async function onSubmit() {
  error.value = ''

  if (!isLogin.value && password.value !== confirm.value) {
    error.value = 'Пароли не совпадают'
    return
  }

  pending.value = true
  try {
    if (isLogin.value) {
      await login(email.value.trim(), password.value)
    } else {
      await register(email.value.trim(), password.value)
    }
    await navigateTo('/')
  } catch (e) {
    error.value = getErrorMessage(e, 'Не удалось выполнить запрос')
  } finally {
    pending.value = false
  }
}
</script>

<style lang="scss" scoped>
.auth {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 24px;

  &__card {
    display: flex;
    flex-direction: column;
    gap: 16px;
    width: 100%;
    max-width: 400px;
    padding: 32px;
    background: rgba($indigo-ink, 0.35);
    border: 1px solid $indigo-velvet;
    border-radius: 16px;
    backdrop-filter: blur(6px);
  }

  &__title {
    margin: 0 0 8px;
    font-size: 26px;
    color: #fff;
    text-align: center;
  }

  &__error {
    margin: 0;
    padding: 10px 12px;
    font-size: 14px;
    color: #ffb4c0;
    background: rgba(#ff4d6d, 0.15);
    border: 1px solid rgba(#ff4d6d, 0.4);
    border-radius: 8px;
  }

  &__switch {
    margin: 0;
    font-size: 14px;
    text-align: center;

    a {
      color: $mauve-magic;
    }
  }
}
</style>
