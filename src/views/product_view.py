from decimal import Decimal

from pony.orm import commit
from pydantic import BaseModel
from fastapi import APIRouter
from starlette.responses import FileResponse, Response
from starlette.requests import Request

from src.models import Product

router = APIRouter()


class ProductM(BaseModel):
    name: str
    price: Decimal
    description: str


@router.post("/product/add")
async def add_user(*, pro: ProductM, request: Request):
    print(request.pony_session)
    with request.pony_session:
        Product(name=pro.name, price=pro.price, description=pro.description)
        commit()

    return Response('{"code":0000,"msg":"OK"}')


