from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_DSN: str
    DEBUG: bool = False
    DB_POOL_SIZE: int = 10
    DB_POOL_PRE_PING: bool = True
    DB_MAX_OVERFLOW: int = 10
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
