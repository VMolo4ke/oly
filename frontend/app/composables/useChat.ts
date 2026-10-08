import type { ChatMessage, ChatRequest, ChatServerEvent } from '~/types'

const WS_UNAUTHORIZED = 4401

let counter = 0
const nextId = () => `${Date.now()}-${counter++}`

// Единственное соединение на вкладку (живёт вне компонентов)
let socket: WebSocket | null = null

export function useChat() {
  const config = useRuntimeConfig()
  const { token, logout } = useAuth()

  const messages = useState<ChatMessage[]>('chat-messages', () => [])
  // Идёт генерация ответа
  const loading = useState('chat-loading', () => false)
  // Запрос отправлен, но первый токен ещё не пришёл
  const waiting = useState('chat-waiting', () => false)

  function wsUrl() {
    const base = String(config.public.apiBase).replace(/^http/, 'ws').replace(/\/$/, '')
    return `${base}/chat/ws?token=${encodeURIComponent(token.value ?? '')}`
  }

  function pushError(content: string) {
    messages.value.push({ id: nextId(), role: 'assistant', content, error: true })
  }

  function finish() {
    loading.value = false
    waiting.value = false
  }

  // Сообщение ассистента, которое сейчас стримится (последнее в списке)
  function currentAssistant(): ChatMessage | undefined {
    const last = messages.value[messages.value.length - 1]
    return last && last.role === 'assistant' && !last.error ? last : undefined
  }

  function handleEvent(event: ChatServerEvent) {
    switch (event.type) {
      case 'start':
        messages.value.push({ id: nextId(), role: 'assistant', content: '' })
        break
      case 'token': {
        waiting.value = false
        const msg = currentAssistant()
        if (msg) {
          msg.content += event.content
        }
        break
      }
      case 'sources': {
        const msg = currentAssistant()
        if (msg) {
          msg.sources = event.sources
        }
        break
      }
      case 'done':
        dropEmptyAssistant()
        finish()
        break
      case 'error':
        dropEmptyAssistant()
        pushError(event.detail)
        finish()
        break
    }
  }

  function dropEmptyAssistant() {
    const msg = currentAssistant()
    if (msg && !msg.content) {
      messages.value.pop()
    }
  }

  async function handleClose(code: number) {
    if (code === WS_UNAUTHORIZED) {
      finish()
      logout()
      await navigateTo('/auth/login')
      return
    }
    if (loading.value) {
      dropEmptyAssistant()
      pushError('Соединение с сервером потеряно')
      finish()
    }
  }

  function connect(): Promise<WebSocket> {
    if (socket && socket.readyState === WebSocket.OPEN) {
      return Promise.resolve(socket)
    }

    return new Promise((resolve, reject) => {
      const ws = new WebSocket(wsUrl())
      ws.onopen = () => {
        socket = ws
        resolve(ws)
      }
      ws.onmessage = (e) => {
        try {
          handleEvent(JSON.parse(e.data) as ChatServerEvent)
        } catch {
          // игнорируем некорректные кадры
        }
      }
      ws.onerror = () => reject(new Error('ws error'))
      ws.onclose = (e) => {
        if (ws === socket) {
          socket = null
        } else {
          // Закрылись до открытия соединения
          reject(new Error('ws closed'))
        }
        void handleClose(e.code)
      }
    })
  }

  async function send(text: string) {
    const content = text.trim()
    if (!content || loading.value) {
      return
    }

    // История — только успешные сообщения, без текущего
    const history = messages.value
      .filter(m => !m.error && m.content)
      .map(({ role, content }) => ({ role, content }))

    messages.value.push({ id: nextId(), role: 'user', content })
    loading.value = true
    waiting.value = true

    try {
      const ws = await connect()
      const payload: ChatRequest = { message: content, history }
      ws.send(JSON.stringify(payload))
    } catch {
      // Если сервер отказал в авторизации, handleClose уже сделал редирект
      if (loading.value) {
        pushError('Не удалось связаться с сервером')
        finish()
      }
    }
  }

  function clear() {
    messages.value = []
  }

  function disconnect() {
    socket?.close()
    socket = null
    finish()
  }

  return { messages, loading, waiting, send, clear, disconnect }
}
