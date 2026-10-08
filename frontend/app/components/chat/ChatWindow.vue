<template>
  <section class="chat">
    <header class="chat__header">
      <div class="chat__user">{{ user?.email }}</div>
      <div class="chat__actions">
        <CommonButton variant="ghost" :disabled="!messages.length || loading" @click="clear">
          Очистить
        </CommonButton>
        <CommonButton variant="ghost" @click="onLogout">Выйти</CommonButton>
      </div>
    </header>

    <div ref="listRef" class="chat__list">
      <p v-if="!messages.length" class="chat__empty">
        Задайте вопрос — ответ придёт от LLM
      </p>

      <ChatMessageItem v-for="m in messages" :key="m.id" :message="m" />

      <div v-if="loading" class="chat__typing">
        <span /><span /><span />
      </div>
    </div>

    <form class="chat__form" @submit.prevent="onSubmit">
      <textarea
        v-model="draft"
        class="chat__input"
        rows="1"
        placeholder="Введите сообщение… (Enter — отправить, Shift+Enter — перенос)"
        :disabled="loading"
        @keydown.enter.exact.prevent="onSubmit"
      />
      <CommonButton type="submit" :disabled="!draft.trim()" :loading="loading">
        Отправить
      </CommonButton>
    </form>
  </section>
</template>

<script setup lang="ts">
const { user, logout } = useAuth()
const { messages, loading, send, clear } = useChat()

const draft = ref('')
const listRef = ref<HTMLElement | null>(null)

async function onSubmit() {
  const text = draft.value
  if (!text.trim() || loading.value) {
    return
  }
  draft.value = ''
  await send(text)
}

async function onLogout() {
  logout()
  clear()
  await navigateTo('/auth/login')
}

// Автопрокрутка вниз при новых сообщениях
watch(
  [() => messages.value.length, loading],
  async () => {
    await nextTick()
    listRef.value?.scrollTo({ top: listRef.value.scrollHeight, behavior: 'smooth' })
  },
  { flush: 'post' }
)
</script>

<style lang="scss" scoped>
.chat {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 900px;
  height: 100vh;
  margin: 0 auto;
  padding: 16px;
  gap: 12px;

  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
  }

  &__user {
    overflow: hidden;
    font-size: 14px;
    color: $mauve-magic;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  &__actions {
    display: flex;
    gap: 8px;
  }

  &__list {
    display: flex;
    flex: 1;
    flex-direction: column;
    gap: 12px;
    padding: 16px;
    overflow-y: auto;
    background: rgba($indigo-ink, 0.2);
    border: 1px solid $indigo-ink;
    border-radius: 16px;
  }

  &__empty {
    margin: auto;
    color: rgba($mauve, 0.6);
  }

  &__typing {
    display: flex;
    gap: 4px;
    padding: 8px 4px;

    span {
      width: 8px;
      height: 8px;
      background: $mauve-magic;
      border-radius: 50%;
      animation: blink 1.2s infinite ease-in-out;

      &:nth-child(2) {
        animation-delay: 0.2s;
      }

      &:nth-child(3) {
        animation-delay: 0.4s;
      }
    }
  }

  &__form {
    display: flex;
    align-items: flex-end;
    gap: 8px;
  }

  &__input {
    flex: 1;
    max-height: 160px;
    padding: 12px 14px;
    color: #fff;
    resize: none;
    background: rgba($dark-amethyst, 0.6);
    border: 1px solid $indigo-velvet;
    border-radius: 10px;
    outline: none;
    field-sizing: content;

    &:focus {
      border-color: $lavender-purple;
      box-shadow: 0 0 0 3px rgba($lavender-purple, 0.25);
    }
  }
}

@keyframes blink {
  0%,
  80%,
  100% {
    opacity: 0.25;
  }

  40% {
    opacity: 1;
  }
}
</style>
