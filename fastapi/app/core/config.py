import secrets
from typing import Any, List, Optional, Union

from dotenv import load_dotenv
from pydantic import (
    AnyHttpUrl,
    EmailStr,
    PostgresDsn,
    ValidationInfo,
    field_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    """
    Settings for the FastAPI application, gets inferred from the environment
    """

    model_config = SettingsConfigDict(case_sensitive=True)
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ALGORITHM: str = "HS256"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    DEBUG_SQL: bool = False
    SKIP_TEST_DB_SETUP: bool = False
    SERVER_HOST: str = "http://127.0.0.1:8000"

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, value: List[str]) -> Union[List[str], str]:
        """
        Checks BACKEND_CORS_ORIGIN is a list of strings
        """
        if isinstance(value, (list, str)):
            return value
        raise ValueError(value)

    PROJECT_NAME: str = "Backbone"

    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    POSTGRES_HOST: Optional[str] = "db"
    POSTGRES_PORT: Optional[int] = 5432
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    SQLALCHEMY_SYNC_DATABASE_URI: Optional[PostgresDsn] = None
    TEST_SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, _: Optional[str], values: ValidationInfo) -> Any:
        host = values.data.get("POSTGRES_HOST")
        port = values.data.get("POSTGRES_PORT") if host != "db" else 5432
        # pylint: disable-next=no-member
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=host,
            path=values.data.get("POSTGRES_DB"),
            port=port,
        )

    @field_validator("SQLALCHEMY_SYNC_DATABASE_URI", mode="before")
    @classmethod
    def assemble_sync_db_connection(
        cls, _: Optional[str], values: ValidationInfo
    ) -> Any:
        host = values.data.get("POSTGRES_HOST")
        port = values.data.get("POSTGRES_PORT") if host != "db" else 5432
        # pylint: disable-next=no-member
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=host,
            path=values.data.get("POSTGRES_DB"),
            port=port,
        )

    @field_validator("TEST_SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_test_db_connection(
        cls, _: Optional[str], values: ValidationInfo
    ) -> Any:
        host = values.data.get("POSTGRES_HOST")
        port = values.data.get("POSTGRES_PORT") if host != "db" else 5432
        # pylint: disable-next=no-member
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=host,
            path=f"test_{values.data.get('POSTGRES_DB')}",
            port=port,
        )

    MINIO_USER: Optional[str] = None
    MINIO_PASSWORD: Optional[str] = None
    MINIO_BUCKET: Optional[str] = None
    MINIO_HOST: Optional[str] = "localhost"
    MINIO_PORT: Optional[str] = "9000"

    SMTP_TLS: bool = False
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None

    @field_validator("SMTP_PORT", mode="before")
    @classmethod
    def validate_smtp_port(cls, val: bool, values: ValidationInfo) -> Any:
        host = values.data.get("SMTP_HOST")
        port = val if host != "mailhog" else 1025
        return port

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "app/utils/email-templates/build"
    EMAILS_ENABLED: bool = False

    @field_validator("EMAILS_ENABLED", mode="before")
    @classmethod
    def get_emails_enabled(cls, _: bool, values: ValidationInfo) -> bool:
        return bool(
            values.data.get("SMTP_HOST")
            and values.data.get("SMTP_PORT")
            and values.data.get("EMAILS_FROM_EMAIL")
        )

    MEILI_MASTER_KEY: str = ""
    MEILI_HOST: str = "localhost"
    MEILI_PORT: int = 7700
    MEILI_TLS: bool = False
    MEILI_URL: str = ""

    @field_validator("MEILI_URL", mode="before")
    @classmethod
    def assemble_meili_url(cls, _: Optional[str], values: ValidationInfo) -> Any:
        scheme = "https" if values.data.get("MEILI_TLS") else "http"
        host = values.data.get("MEILI_HOST")
        port = values.data.get("MEILI_PORT") if host != "meilisearch" else 7700
        return f"{scheme}://{host}:{port}"

    FGA_API_SCHEME: str = "http"
    FGA_API_HOST: str = "localhost"
    FGA_API_PORT: int = 8080
    FGA_STORE_ID: str = ""
    FGA_AUTHN_PRESHARED_KEY: str = ""
    FGA_MODEL_ID: str = ""

    @field_validator("FGA_API_PORT", mode="before")
    @classmethod
    def validate_fga_api_port(cls, val: Optional[str], values: ValidationInfo) -> Any:
        host = values.data.get("FGA_API_HOST")
        if host == "openfga":
            return 8080
        return val


settings = Settings()
