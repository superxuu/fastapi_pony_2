from datetime import datetime

from pony.orm import PrimaryKey, Required, Optional, Set, LongStr

from src.models import db, Role


class Permission(db.Entity):
    permission_id = PrimaryKey(int)
    role = Set(Role)
    description = Optional(LongStr)
    create_time = Required(datetime, default=datetime.now)
    update_time = Optional(datetime)

    def before_update(self):
        self.update_time = datetime.now()
