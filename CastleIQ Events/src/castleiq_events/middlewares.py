from fastapi import Request, Response
from starlette.datastructures import MutableHeaders

from .events import RaisedEvent


async def capture_error_events_middleware(request: Request, call_next):
    try:
        response: Response = await call_next(request)
    except RaisedEvent as ev:

        response = Response(status_code=ev.data.status_code, content=ev.data.json(),
                            headers=MutableHeaders({'content-type': 'application/json'}))

    return response
