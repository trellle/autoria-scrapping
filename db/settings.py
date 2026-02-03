from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class PostgreSQLSettings(BaseSettings):
    POSTGRES_DB: str = "autoria"
    POSTGRES_USER: str = "default_user"
    POSTGRES_DB_PORT: int = 5432
    POSTGRES_PASSWORD: str = "default_password"
    POSTGRES_HOST: str = "127.0.0.1"


settings = PostgreSQLSettings()
DATABASE_URL = (
    f"postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
    f"{settings.POSTGRES_HOST}:{settings.POSTGRES_DB_PORT}/{settings.POSTGRES_DB}"
)
