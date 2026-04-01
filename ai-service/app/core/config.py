from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "hearing-ai-service"
    app_env: str = "development"
    port: int = 8001

    ai_shared_token: str = "change-me"
    backend_internal_url: str = "http://localhost:8000"
    backend_api_key: str = "change-me"

    stt_provider: str = "dummy"
    stt_language: str = "ko"
    forward_timeout_sec: int = 10
    min_confidence: float = 0.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()