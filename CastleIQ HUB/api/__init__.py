from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from castleiq_events.middlewares import capture_error_events_middleware
from core.apps import include_apps
from config import conf


app = FastAPI(
    debug=conf.debug,
    title="CastleIQ HUB",
    description="Smart home server",
    version=conf.version)


app.middleware("http")(capture_error_events_middleware)

# origins = [
#     "http://127.0.0.1",
#     "https://127.0.0.1"
#     "http://127.0.0.1:5173",
#     "https://127.0.0.1:5173",
#     "https://localhost:5173",
#     "http://localhost:5173",
#     "http://localhost",
#     "https://localhost",
#     "http://10.10.10.14",
#     "https://10.10.10.14",
# ]

# origins = [
#     "*"
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def hello_world():
    return {"message": "Hello world"}


@app.get("/test")
async def test():
    return {"a": "b"}


if __name__ == "api":
    include_apps(app, conf.apps)
