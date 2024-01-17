from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongo_uri: str
    postgres_uri: str
    api_v1_prefix: str
    jwt_secret_key: str
    jwt_algorith: str
    token_expiration_time: int = 30
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
