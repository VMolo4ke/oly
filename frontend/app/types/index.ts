export interface User {
  id: number
  email: string
  is_active: boolean
  created_at: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export type ChatRole = 'user' | 'assistant'

export interface ChatSource {
  article_id: number
  title: string
}

export interface ChatMessage {
  id: string
  role: ChatRole
  content: string
  error?: boolean
  sources?: ChatSource[]
}

// Клиент -> сервер (WebSocket)
export interface ChatRequest {
  message: string
  history: Array<{ role: ChatRole, content: string }>
}

// Сервер -> клиент (WebSocket)
export type ChatServerEvent
  = | { type: 'start' }
    | { type: 'token', content: string }
    | { type: 'sources', sources: ChatSource[] }
    | { type: 'done' }
    | { type: 'error', detail: string }
