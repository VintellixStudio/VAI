from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Vintellix AI Agent"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True


settings = Settings()