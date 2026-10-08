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

export interface ChatMessage {
  id: string
  role: ChatRole
  content: string
  error?: boolean
}

export interface ChatRequest {
  message: string
  history: Array<{ role: ChatRole, content: string }>
}

export interface ChatResponse {
  answer: string
}
