
from pydantic import ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file='.env')

    database_hostname: str 
    database_port: str 
    database_username: str 
    database_password: str 
    database_name: str 
    secret_key: str 
    access_token_expire_minutes: int 
    algorithm: str 

   

settings = Settings()

