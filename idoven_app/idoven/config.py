from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongo_uri: str
    api_v1_prefix: str = "/api/v1"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
