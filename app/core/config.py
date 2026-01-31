from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Smart Task Manager"
    debug: bool = False

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/tasks_db"

    gemini_api_key: str
    gemini_model: str = "gemini-1.5-flash"

    class Config:
        env_file = ".env"

settings = Settings()