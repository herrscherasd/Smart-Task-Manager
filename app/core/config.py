from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Smart Task Manager"
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()