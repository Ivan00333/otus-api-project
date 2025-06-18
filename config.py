import os
from dotenv import load_dotenv
from pydantic import HttpUrl, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class HTTPClientConfig(BaseModel):
    url: HttpUrl
    timeout: float

    @property
    def client_url(self):

        return str(self.url)

env = os.getenv("ENV", "test")

class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='__'
    )

    users_client: HTTPClientConfig