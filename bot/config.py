from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Bot(BaseModel):
    token: str = ""


class WebApp(BaseModel):
    base_url: str = ""


class Api(BaseModel):
    base_url: str = ""
    token: str = ""
    face_recognition_prefix: str = ""


class S3(BaseModel):
    key_id: str = ""
    access_key: str = ""
    endpoint: str = ""
    region_name: str = ""
    basket_name: str = ""


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("bot/.env.template", "bot/.env"),
        env_file_encoding='utf-8',
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    bot: Bot = Bot()
    web_app: WebApp = WebApp()
    api: Api = Api()
    s3: S3 = S3()


settings = Settings()
