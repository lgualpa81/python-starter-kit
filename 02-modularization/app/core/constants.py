from typing import Literal
from enum import Enum

MEDIA_DIR = "app/media"


class RoleEnum(Enum):
    user = 0
    editor = 1
    admin = 2
