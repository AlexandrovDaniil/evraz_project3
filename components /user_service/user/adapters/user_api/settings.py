from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    IS_DEV_MODE: bool = True
