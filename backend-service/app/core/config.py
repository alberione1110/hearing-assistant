from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    app_name: str = 'hearing-backend-service'
    app_env: str = 'development'
    api_key: str = 'change-me'
    database_url: str = 'postgresql+psycopg://postgres:postgres@localhost:5432/hearing_assistant'
    backend_cors_origins: List[str] | str = Field(default_factory=lambda: ['*'])

    def cors_origins(self) -> List[str]:
        if isinstance(self.backend_cors_origins, str):
            if self.backend_cors_origins.strip() == '*':
                return ['*']
            return [origin.strip() for origin in self.backend_cors_origins.split(',') if origin.strip()]
        return self.backend_cors_origins


settings = Settings()
