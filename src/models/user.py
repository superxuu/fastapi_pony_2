from datetime import datetime
from enum import Enum

from pony.orm import PrimaryKey, Required, Optional, Set, LongStr, commit
from pony.orm.dbapiprovider import StrConverter, Converter

from src.models import db


class State(Enum):
    disable = 0
    enable = 1


class StateConverter(StrConverter):

    def validate(self, val, obj=None):
        if State(val) not in State:
            # if not isinstance(val, State):
            raise ValueError('Must be an State.  Got {}'.format(type(val)))
        return val

    def py2sql(self, val):
        return val

    def sql2py(self, value):
        return self.py_type(int(value)).value


db.provider.converter_classes.append((Enum, StateConverter))


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    # name = Set('Role')
    name = Required(str, unique=True, max_len=30)
    pwd = Required(str, max_len=100)
    email = Optional(str, max_len=50)
    state = Required(State)
    role = Optional(int)
    create_time = Required(datetime, default=datetime.now)
    update_time = Optional(datetime)

    def before_update(self):
        self.update_time = datetime.now()
