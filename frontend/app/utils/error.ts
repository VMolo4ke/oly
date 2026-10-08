interface FetchErrorLike {
  statusCode?: number
  data?: { detail?: unknown }
}

/**
 * Достаёт читаемое сообщение из ошибки $fetch / FastAPI
 * (detail может быть строкой или списком ошибок валидации pydantic).
 */
export function getErrorMessage(error: unknown, fallback = 'Что-то пошло не так'): string {
  const err = error as FetchErrorLike | undefined
  const detail = err?.data?.detail

  if (typeof detail === 'string') {
    return detail
  }
  if (Array.isArray(detail) && detail.length) {
    return detail
      .map((item: { msg?: string }) => item?.msg)
      .filter(Boolean)
      .join('; ') || fallback
  }
  if (err?.statusCode === undefined) {
    return 'Не удалось связаться с сервером'
  }
  return fallback
}
