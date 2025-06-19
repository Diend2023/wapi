from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    items_per_page: int = 50
    host: str = "127.0.0.1"
    port: int = 2577

settings = Settings()