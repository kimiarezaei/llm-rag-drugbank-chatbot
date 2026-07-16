from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    # API Keys
    model_config = SettingsConfigDict(env_file=".env")
    anthropic_api_key: str
    hf_token: str | None = None

    # LLM
    model_name: str = "claude-sonnet-4-6"
    temperature: float = 0.0
    max_tokens: int = 500

    # QA
    qa_temperature: float = 0.0
    qa_max_tokens: int = 600

    # Embeddings
    embedding_model_name: str = "all-MiniLM-L6-v2"


    # question keyword extraction
    keyword_temperature: float = 0.0
    keyword_max_tokens: int = 200


    # Cache
    cache_version: str = "v1"

    @computed_field
    @property
    def cache_file(self) -> str:
        return f"cache/data_cache_{self.cache_version}.json"

    @computed_field
    @property
    def chroma_path(self) -> str:
        return f"chromadb_{self.cache_version}"

    @computed_field
    @property
    def log_file(self) -> str:
        return "logs/app.log"

    


settings = Settings()