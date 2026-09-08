from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    gemini_api_key :str
    model_name: str = "gemini-3.8-flash"
    database_url : str

    class Config:
        env_file = ".env"