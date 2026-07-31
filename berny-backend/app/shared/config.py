from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    WORKER_ID: int = 1

    SCYLLA_IP: str = "127.0.0.1"
    SCYLLA_PORT: int = 9042
    SCYLLA_KEYSPACE: str = "berny"
    SCYLLA_REPLICATION_FACTOR: int = 1
    SCYLLA_CLASS: str = "NetworkTopologyStrategy"

    POSTGRES_USER: str = "myuser"
    POSTGRES_PASSWORD: str = "mypassword"
    POSTGRES_DB: str = "mydb"
    POSTGRES_PORT: int = 5432
    POSTGRES_HOST: str = "localhost"

    CLIENT_ID: str = "YOUR_APP_ID.apps.googleusercontent.com"

    SECRET_JWT: str = "mysecretkey"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
