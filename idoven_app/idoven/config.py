from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongo_uri: str = "mongodb://mongo:27017/ecg"
    postgres_uri: str = "postgresql://postgres:postgres@localhost/postgres"
    api_v1_prefix: str = "/api/v1"
    jwt_secret_key = "adba27e22c8cff65dd8e713bce6383c789eadcae6c95945ceab3c94a2697b8d9"
    jwt_algorith = "HS256"
    token_expiration_time = 30


settings = Settings()
