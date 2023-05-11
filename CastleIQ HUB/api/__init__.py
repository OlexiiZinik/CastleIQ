from fastapi import FastAPI

from  core.apps import include_apps

from config import conf
from logger import logger


app = FastAPI(
    debug=conf.debug,
    title="CastleIQ HUB",
    description="Smart home server",
    version=conf.version)


@app.get("/")
async def hello_world():
    return {"message": "Hello world"}


@app.post("/test")
async def hello_world(param1: int, param2: int):
    return {"message": "Hello world", "param1": param1, "param2": param2}


if __name__ == "api":
    include_apps(app, conf.apps)
