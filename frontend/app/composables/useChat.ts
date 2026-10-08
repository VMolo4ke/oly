import type { ChatMessage, ChatRequest, ChatResponse } from '~/types'

let counter = 0
const nextId = () => `${Date.now()}-${counter++}`

export function useChat() {
  const config = useRuntimeConfig()
  const { token, logout } = useAuth()

  const messages = useState<ChatMessage[]>('chat-messages', () => [])
  const loading = ref(false)

  async function send(text: string) {
    const content = text.trim()
    if (!content || loading.value) {
      return
    }

    // История — только успешные сообщения, без текущего
    const history = messages.value
      .filter(m => !m.error)
      .map(({ role, content }) => ({ role, content }))

    messages.value.push({ id: nextId(), role: 'user', content })
    loading.value = true

    try {
      const body: ChatRequest = { message: content, history }
      const data = await $fetch<ChatResponse>('/chat', {
        baseURL: config.public.apiBase,
        method: 'POST',
        headers: { Authorization: `Bearer ${token.value}` },
        body
      })
      messages.value.push({ id: nextId(), role: 'assistant', content: data.answer })
    } catch (error) {
      if ((error as { statusCode?: number }).statusCode === 401) {
        logout()
        await navigateTo('/auth/login')
        return
      }
      messages.value.push({
        id: nextId(),
        role: 'assistant',
        content: getErrorMessage(error, 'Не удалось получить ответ от модели'),
        error: true
      })
    } finally {
      loading.value = false
    }
  }

  function clear() {
    messages.value = []
  }

  return { messages, loading, send, clear }
}
