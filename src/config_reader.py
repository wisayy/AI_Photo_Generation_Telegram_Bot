
import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    DB_URL: SecretStr
    REPLICATE_API_TOKEN: SecretStr
    STRIPE_API_KEY: SecretStr
    YOOMONEY_API_KEY: SecretStr

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), ".env"), #python src/__main__.py
        env_file_encoding="utf-8"
    )

config = Settings()

