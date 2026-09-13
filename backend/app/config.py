from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Real Estate Intelligence API"
    app_version: str = "0.1.0"
    database_url: str = "sqlite:///./data/realestate.db"
    chroma_path: str = "./data/chroma"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen3:4b"
    embedding_model: str = "nomic-embed-text"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
