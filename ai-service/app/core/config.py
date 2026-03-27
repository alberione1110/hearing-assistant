from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    app_name: str = 'hearing-ai-service'
    app_env: str = 'development'
    ai_shared_token: str = 'change-me'
    backend_internal_url: str = 'http://localhost:8000'
    backend_api_key: str = 'change-me'


settings = Settings()
