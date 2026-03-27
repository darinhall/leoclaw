from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "LeoClaw Orchestrator"
    debug: bool = False

    host: str = "0.0.0.0"
    port: int = 8000

    # Where the lume-client polls for tasks
    task_queue_max_size: int = 100

    # Ollama (added in Step 8 — optional for now)
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3"

    # Postgres (added in Step 10)
    database_url: str = "postgresql+asyncpg://leoclaw:leoclaw@localhost:5432/leoclaw"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
