from pydantic_settings import BaseSettings, SettingsConfigDict

class LLMSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    SUPABASE_CONNECTION_STRING: str
    GOOGLE_API_KEY: str

settings = LLMSettings()
