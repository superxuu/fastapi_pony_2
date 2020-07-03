from typing import Optional

from fastapi import APIRouter, Path, Query, Depends
from pony.orm import commit
from pydantic.fields import Field
from starlette.responses import FileResponse, Response
from src.utils.security import *

router = APIRouter()


class UserM(BaseModel):
    name: str = Field(..., title="User Name", max_length=30)
    pwd: str = Field('123456', title="User pwd", max_length=100)
    email: str = Field(None, title="User email", max_length=50)
    state: int = Field(1, title="User state")
    # state: Optional[int] = 1
    role: int = Field(3, title="User role")


@router.post("/add", dependencies=[Security(get_current_active_user, scopes=['5'])],
             summary="新增一个用户", )
async def add_user(*, user: UserM, request: Request):
    try:
        with request.pony_session:
            if Role[user.role]:
                if user.email:
                    User(name=user.name, pwd=get_password_hash(user.pwd), state=user.state, email=user.email,
                         role=user.role)
                else:
                    User(name=user.name, pwd=get_password_hash(user.pwd), state=user.state, role=user.role)
                # commit()
            # else:
            #     return Response(f'{{"code":0001,"msg":"Role id {user.role} not exist"}}')
        return Response('{"code":0000,"msg":"user add OK"}')
    except Exception as e:
        import traceback
        raise HTTPException(status_code=400, detail=traceback.print_exc())
        # raise HTTPException(status_code=400, detail=f"user add error: {e}")


@router.get("/info", response_model=UserM, response_model_exclude={"pwd"},
            dependencies=[Security(get_current_active_user, scopes=['1', '2', '3'])], summary="查询一个用户信息")
async def get_user(*, user_name, request: Request):
    try:
        with request.pony_session:
            user = User.get(name=user_name)
        if user:
            return user.to_dict()
        else:
            return Response(f'{{"code":0001,"msg":"user {user_name} not exist"}}')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"user info error: {e}")


@router.delete("/del", dependencies=[Security(get_current_active_user, scopes=['1', '2', '3', '4', '5'])],
               summary="删除一个用户", description="根据用户名称来删除一个用户！")
async def del_user(*, user_name, request: Request):
    try:
        with request.pony_session:
            user = User.get(name=user_name)
            if user:
                user.delete()
                commit()
                return Response(f'{{"code":0000,"msg":"user {user_name} delete success"}}')
            else:
                return Response(f'{{"code":0001,"msg":"user {user_name} not exist"}}')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"user delete error: {e}")


@router.put("/update", response_model=UserM, response_model_exclude={"pwd"},
            dependencies=[Security(get_current_active_user, scopes=['1', '2', '3'])],
            summary="更新一个用户", description="根据用户名称来更新用户的其他信息！")
async def update_user(*, user: UserM, request: Request):
    user = user.dict(exclude_unset=True)
    print(user)
    try:
        with request.pony_session:
            u = User.get(name=user['name'])
            if not user:
                return Response(f'{{"code":0001,"msg":"user {user.name} not exist"}}')
            if user.get('role') and Role[user.get('role')]:
                u.role = user['role']
            if user.get('pwd'):
                u.pwd = get_password_hash(user['pwd'])
            if user.get('email'):
                u.email = user['email']
            if user.get('state'):
                u.state = user['state']
        return u.to_dict()
                # return Response(f'{{"code":0000,"msg":"user {user.name} update OK", "user":{UserM(**u.to_dict())}}}')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"user update error: {e}")


@router.post("/login", response_model=Token, summary="用户登录",
             description="登录成功，获取token")  # , include_in_schema=False, deprecated=True,
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    scopes = get_user_scope(user.name)
    access_token = create_access_token(
        data={"sub": user.name, "scopes": scopes},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
