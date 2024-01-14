from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongo_uri: str = "mongodb://mongo:27017/ecg"
    api_v1_prefix: str = "/api/v1"

settings = Settings()
