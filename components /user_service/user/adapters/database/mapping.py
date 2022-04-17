from sqlalchemy.orm import registry
from user.application import dataclasses

from . import tables

mapper = registry()

mapper.map_imperatively(dataclasses.User, tables.USER)
