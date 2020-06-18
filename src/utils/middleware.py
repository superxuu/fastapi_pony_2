from pony.orm import db_session
from starlette.requests import Request

from run import app


def _enter_session():
    session = db_session()
    Request.pony_session = session
    session.__enter__()


def _exit_session():
    session = getattr(Request, 'pony_session', None)
    if session is not None:
        session.__exit__()


@app.middleware("http")
async def add_pony(request: Request, call_next):
    _enter_session()
    response = await call_next(request)
    _exit_session()
    return response
