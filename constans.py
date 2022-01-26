import enum
from app import db


class UsersRolesEnum(enum.Enum):
    ADMIN = "admin"
    USER = "user"

[(1, 'до 12'), (2, 'до 16'), (3, 'страше 16')]
[(1, "до 12"), (2, "до 16"), (3, "старше 16")]