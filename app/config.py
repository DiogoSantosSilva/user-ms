from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str
    ENVIRONMENT: str
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    HOST: str
    PORT: int

    class Config:
        env_file = ".env"


settings = Settings()
