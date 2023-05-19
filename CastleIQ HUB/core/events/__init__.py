from fastapi import Request, Response
from starlette.datastructures import MutableHeaders

from logger import logger
from core.events import events


async def capture_error_events_middleware(request: Request, call_next):

    try:
        response: Response = await call_next(request)
        logger.info(response)
        logger.info(response.headers)
        logger.info(response.status_code)
    except events.RaisedEvent as ev:
        logger.info(ev.data.dict())
        response = Response(status_code=ev.data.status_code, content=ev.data.json(),
                            headers=MutableHeaders({'content-type': 'application/json'}))

    return response
