from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_dsn: SecretStr = SecretStr("postgresql://alice:xyz@localhost:5432/url")
    validate_redirects: bool = True

    suffix_length: int = Field(default=16, ge=8, le=32)


settings = Settings()
