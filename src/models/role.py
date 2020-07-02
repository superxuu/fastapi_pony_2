from datetime import datetime
from enum import Enum
from pony.orm import PrimaryKey, Required, Optional, Set, LongStr, select
from pony.orm.dbapiprovider import StrConverter

from src.models import db


#
#
# class Role(Enum):
#     admin = 1
#     leader = 2
#     test = 3
#
#
# class RoleConverter(StrConverter):
#
#     def validate(self, val, obj=None):
#         try:
#             if eval(f'State.{val}'):
#                 return val
#         except:
#             raise ValueError(f'{val} not in Role')
#
#     def py2sql(self, val):
#         return val
#
#     def sql2py(self, value):
#         return eval(f'self.py_type.{value}').name
#
#
# db.provider.converter_classes.append(RoleConverter)


class Role(db.Entity):
    id = PrimaryKey(int)
    role = Required(str)
    permissions = Set('Permission')
    create_time = Required(datetime, default=datetime.now)
    update_time = Optional(datetime)

    @staticmethod
    def get_role_permission(id):
        print('id:', id)
        return select(p.permissions.permission_id for p in Role if p.id == id)

    def before_update(self):
        self.update_time = datetime.now()
