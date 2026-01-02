from pydantic_settings import BaseSettings
from pydantic import SecretStr

# Settings which pull vars from .env file, have default values which can be OVERRIDEN BY .env
class AppSettings(BaseSettings):
    POSTGRES_CONNECTION_STRING: SecretStr
    # TODO: Add logging and tracing
    # LOGGER_NAME: str = "marketing-api-logger"
    # TRACER_NAME: str = "marketing-api-tracer"
    JWT_SECRET_KEY: SecretStr
    JWT_ALGORITHM: str = "HS256"
    PASSWORD_SALT: SecretStr
    PASSWORD_SALT_ROUNDS: int = 12
    
    class Config:
        env_file = ".env"

app_settings = AppSettings()