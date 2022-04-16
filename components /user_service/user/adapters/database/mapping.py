from user.application import dataclasses
from sqlalchemy.orm import registry

from . import tables

mapper = registry()

mapper.map_imperatively(dataclasses.User, tables.USER)


