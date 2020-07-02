from fastapi import APIRouter, Path, Query, Depends
from pony.orm import commit, select
from pydantic.fields import Field
from starlette.responses import FileResponse, Response

from src.models import Role, Permission
from src.utils.security import *

router = APIRouter()


class RoleM(BaseModel):
    user_name: str
    role: str

@router.post('/add')
async def assign_permission(*, role: str, permission_id: List[int], request: Request):
    with request.pony_session:
        permission_db_id = select(p.permission_id for p in Permission)
        print('permission_db_id:', permission_db_id)
        print(1 in permission_db_id)
        for p_id in permission_id:
            if p_id in permission_db_id:
                pass
