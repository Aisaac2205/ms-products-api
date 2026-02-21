from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://testuser:testpass@localhost:5432/productsdb"
    SECRET_KEY: str = "change-this-secret-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Usuario admin por defecto para el pipeline de tests
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin1234"

    class Config:
        env_file = ".env"


settings = Settings()
