from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str
    DEBUG: bool
    VERSION: str
    ENVIRONMENT: str
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    REDIS_URL: str
    APP_VERSION: str
    APP_ENV: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
