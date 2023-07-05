from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

class Settings(BaseSettings):

    class Config:
        env_file = ".env"  # Especifique o caminho para o arquivo .env

settings = Settings()
