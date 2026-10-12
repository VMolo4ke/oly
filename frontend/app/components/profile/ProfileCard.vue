<template>
  <div class="profile">
    <section class="profile__card">
      <div class="profile__head">
        <div class="profile__avatar" aria-hidden="true">{{ initial }}</div>
        <div class="profile__identity">
          <h1 class="profile__email">{{ user?.email }}</h1>
          <span
            class="profile__badge"
            :class="{ 'profile__badge--off': user && !user.is_active }"
          >
            {{ user?.is_active ? 'Аккаунт активен' : 'Аккаунт отключён' }}
          </span>
        </div>
      </div>

      <dl class="profile__list">
        <div class="profile__row">
          <dt>ID пользователя</dt>
          <dd>{{ user?.id }}</dd>
        </div>
        <div class="profile__row">
          <dt>Дата регистрации</dt>
          <dd>
            <ClientOnly>
              {{ createdAt }}
              <template #fallback>—</template>
            </ClientOnly>
          </dd>
        </div>
        <div class="profile__row">
          <dt>Сообщений в текущей сессии</dt>
          <dd>{{ messages.length }}</dd>
        </div>
      </dl>

      <div class="profile__actions">
        <CommonButton @click="navigateTo('/')">К чату</CommonButton>
        <CommonButton
          variant="ghost"
          :disabled="!messages.length || loading"
          @click="clear"
        >
          Очистить историю чата
        </CommonButton>
        <CommonButton variant="ghost" @click="onLogout">Выйти</CommonButton>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
const { user, logout } = useAuth()
const { messages, loading, clear, disconnect } = useChat()

const initial = computed(() => user.value?.email?.charAt(0).toUpperCase() ?? '?')

const createdAt = computed(() => {
  if (!user.value?.created_at) {
    return '—'
  }
  const date = new Date(user.value.created_at)
  if (Number.isNaN(date.getTime())) {
    return '—'
  }
  return date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' })
})

async function onLogout() {
  disconnect()
  logout()
  clear()
  await navigateTo('/auth/login')
}
</script>

<style lang="scss" scoped>
.profile {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 24px;

  &__card {
    display: flex;
    flex-direction: column;
    gap: 24px;
    width: 100%;
    max-width: 480px;
    padding: 32px;
    background: rgba($surface, 0.85);
    border: 1px solid $border;
    border-radius: 16px;
    box-shadow: 0 8px 28px rgba($green-700, 0.08);
    backdrop-filter: blur(6px);
  }

  &__head {
    display: flex;
    gap: 16px;
    align-items: center;
  }

  &__avatar {
    display: flex;
    flex-shrink: 0;
    align-items: center;
    justify-content: center;
    width: 64px;
    height: 64px;
    font-size: 28px;
    font-weight: 600;
    color: $green-700;
    background: $green-200;
    border: 1px solid $green-300;
    border-radius: 50%;
  }

  &__identity {
    display: flex;
    flex-direction: column;
    gap: 6px;
    align-items: flex-start;
    min-width: 0;
  }

  &__email {
    max-width: 100%;
    margin: 0;
    overflow: hidden;
    font-size: 20px;
    color: $green-700;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  &__badge {
    padding: 2px 10px;
    font-size: 12px;
    color: $green-700;
    background: $green-100;
    border-radius: 999px;

    &--off {
      color: $error-text;
      background: $error-bg;
    }
  }

  &__list {
    display: flex;
    flex-direction: column;
    margin: 0;
    background: $surface;
    border: 1px solid $border;
    border-radius: 12px;
  }

  &__row {
    display: flex;
    gap: 12px;
    align-items: center;
    justify-content: space-between;
    padding: 12px 16px;
    font-size: 14px;

    & + & {
      border-top: 1px solid $border;
    }

    dt {
      color: $text-muted;
    }

    dd {
      margin: 0;
      color: $text;
      text-align: right;
    }
  }

  &__actions {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
}
</style>
