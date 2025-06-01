from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseModel):
    password: str
    user: str = "postgres"
    host: str = "db"
    port: int = 5432
    dbname: str = "postgres"

    @property
    def async_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    database: DBSettings
    api_access_key: str


settings = Settings()
