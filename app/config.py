from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_password: str
    secret_key: str
    database_name: str
    database_port: str
    database_username: str
    algorithm: str
    access_token_expire: int
    
    class Config:
        env_file = ".env"
    
settings = Settings()

