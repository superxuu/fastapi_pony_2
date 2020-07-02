from fastapi import FastAPI

from src.views import user, product_view, role


def create_app():
    app = FastAPI(title='FastApi pony study',
                  description='这是使用fastapi与pony orm进行实践的项目',
                  version=0.1)

    app.include_router(
        user.router,
        prefix="/user",
        tags=["user"],
        dependencies=[],
        responses={404: {"description": "Not found"},500: {"description": "Not found"}},

    )
    app.include_router(
        role.router,
        prefix="/role",
        tags=["role"],
        dependencies=[],
        responses={404: {"description": "Not found"}},

    )

    app.include_router(
        product_view.router,
        prefix="/user",
        tags=["items"],
        dependencies=[],
        responses={404: {"description": "Not found"}},

    )
    return app
