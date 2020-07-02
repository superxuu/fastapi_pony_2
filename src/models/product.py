from datetime import datetime
from decimal import Decimal

from src.models import db, Required, Optional


class Product(db.Entity):
    name = Required(str, unique=True)
    price = Required(Decimal)
    description = Optional(str)
    create_time = Required(datetime, default=datetime.now, precision=6)
    update_time = Optional(datetime)
