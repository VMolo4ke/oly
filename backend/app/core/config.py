from pathlib import Path
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict

_ENV_FILE = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SECRET_KEY: str = "dev-secret-change-me-use-32bytes-min"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    LLM_BASE_URL: str = "https://api.proxyapi.ru/v1"
    LLM_API_KEY: str = "sk-tl70jM95Ruverwg7dbbbTti3ihkXrCor"
    LLM_MODEL: str = "qwen/qwen3.7-flash"
    # Сколько чанков из всех статей подмешивать в контекст
    CHAT_TOP_K: int = 5
    # Макс. косинусное расстояние (0 — идентично, 2 — противоположно).
    # None — не отсекать; например 0.6 отфильтрует нерелевантные чанки.
    CHAT_MAX_DISTANCE: float | None = None

    @property
    def DATABASE_URL(self) -> str:
        password = quote_plus(self.POSTGRES_PASSWORD)
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{password}"
            f"@localhost:5432/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(env_file=_ENV_FILE, extra="ignore")


settings = Settings()
