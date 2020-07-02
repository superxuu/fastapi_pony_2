from src.models.db_factory import db
from pony.orm import db_session, TransactionIntegrityError

from .user import *
from .role import *
from .permission import *
from .product import *

db.generate_mapping(create_tables=True)


try:
    #向user表铺数,管理员账号,密码：qq123456
    with db_session:
        User(name='xuchao', pwd='$2b$12$ELdmKf.DktXaJbEPZThCgeADWrhvwLZm7WTF3UlbDrfH6ua/tmkG2', email='xuchao@ect888.com', state=1, role=1)
except TransactionIntegrityError:
    pass


try:
    # 向权限表铺数
    with db_session:
        Permission(permission_id=1, description='权限1')
        Permission(permission_id=2, description='权限2')
        Permission(permission_id=3, description='权限3')
        Permission(permission_id=4, description='权限4')
        Permission(permission_id=5, description='权限5')
except TransactionIntegrityError:
    pass

admin = [1, 2, 3, 4, 5]
leader = [1, 2, 3]
tester = [1, 2]
try:
    # 像角色表铺数
    with db_session:
        p1 = [p for i in admin for p in Permission.select() if p.permission_id == i]
        Role(id=1, role='admin', permissions=p1)

        p2 = [p for i in leader for p in Permission.select() if p.permission_id == i]
        Role(id=2, role='leader', permissions=p2)

        p3 = [p for i in tester for p in Permission.select() if p.permission_id == i]
        Role(id=3, role='tester', permissions=p3)
except TransactionIntegrityError:
    pass
