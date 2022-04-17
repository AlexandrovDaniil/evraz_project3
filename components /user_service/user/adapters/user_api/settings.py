from typing import Tuple, Union

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    IS_DEV_MODE: bool = True
    ALLOW_ORIGINS: Union[str, Tuple[str, ...]] = Field(default_factory=tuple)
