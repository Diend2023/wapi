from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "wapi"
    admin_email: str = "2577569250@qq.com"
    items_per_page: int = 50
    host: str = "127.0.0.1"
    port: int = 2577

    class Config:
        env_file = ".env"

settings = Settings()