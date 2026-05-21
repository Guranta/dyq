from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "大云雀 API"
    api_prefix: str = "/api/v1"
    ai_provider: str = "mock"
    ai_base_url: str = ""
    ai_api_key: str = ""
    ai_image_model: str = "mock-image"
    ai_video_model: str = "mock-video"
    ai_image_path: str = "/images/generations"
    ai_video_path: str = "/videos/generations"
    output_dir: Path = Path("outputs")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.output_dir.mkdir(parents=True, exist_ok=True)
    return settings
