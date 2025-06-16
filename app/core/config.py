from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    items_per_page: int = 50
    host: str = "::"
    port: int = 2577

settings = Settings()