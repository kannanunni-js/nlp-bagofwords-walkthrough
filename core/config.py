import os
from pathlib import Path
from typing import Literal, Self, cast

from pydantic import EmailStr, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str="BAG OF WORDS"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "v1"
    DEBUG: str = "off"
    WS_MAX_QUEUE: int = 100
    LOG_LEVEL: Literal["critical", "error", "warning", "info", "debug", "trace"] = ("debug")
    FORWARDED_ALLOW_IPS: list[str] | str = "*"
    ENVIRONMENT: Literal["local", "production"] = "local"
    CONCURRENT_THREAD_COUNT: int = 100

    # Uvicorn
    UVICORN_HOST: str = "127.0.0.1"
    UVICORN_PORT: int = 8000
    WORKERS: int = 1

    OPENAI_API_KEY: str = ""
    CORPUS_FILE_PATH: Path = Path.cwd() / "datas" / "corpus"  #-> resolves relative to where you run the app

    model_config = SettingsConfigDict(
        validate_default=False,
        env_prefix="",
        case_sensitive=False,
        extra="ignore",
        env_ignore_empty=True,
    )

    @model_validator(mode="after")
    def check_worker_config(self) -> Self:
        """

        :return:
        """
        # Binding open-akey with OS Environment

        os.environ.setdefault("OPENAI_API_KEY", cast(str, self.OPENAI_API_KEY))
        return self


# Missing named arguments are filled with environment variables
settings = Settings()  # type: ignore[call-arg]
