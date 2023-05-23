from fastapi import FastAPI

from core.events import capture_error_events_middleware
from core.apps import include_apps
from config import conf


app = FastAPI(
    debug=conf.debug,
    title="CastleIQ HUB",
    description="Smart home server",
    version=conf.version)


app.middleware("http")(capture_error_events_middleware)


@app.get("/")
async def hello_world():
    return {"message": "Hello world"}


@app.get("/test")
async def test():
    return {"a": "b"}


if __name__ == "api":
    include_apps(app, conf.apps)
