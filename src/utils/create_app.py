from fastapi import FastAPI

from src.views import route_func


def create_app():
    app = FastAPI(title='FastApi pony study',
                  description='这是使用fastapi与pony orm进行实践的项目',
                  version=0.1)

    app.include_router(
        route_func.router,
        prefix="/items",
        tags=["items"],
        dependencies=[],
        responses={404: {"description": "Not found"}},

    )
    return app
