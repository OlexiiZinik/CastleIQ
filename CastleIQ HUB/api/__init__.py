
from fastapi import Depends, HTTPException, status
from tortoise.exceptions import IntegrityError
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from config import conf
import importlib
from logger import logger
from .authentication.handlers import APIView, ModelView, ModelCreateAndGetView
from .authentication.models import User, UserPydantic, UserInPydantic


app = FastAPI(
    debug=conf.debug,
    title="Hello",
    description="Test",
    version=conf.version)

@app.post("/test", response_model=UserPydantic)
async def create_user(user: UserInPydantic) -> UserPydantic:
    logger.info(user.dict())
    u = await User.create(**user.dict())
    logger.info(u)
    try:
        await u.save()
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User with username '
                                                                            f'{user.username} already exists')
    logger.info(u)
    return await UserPydantic.from_tortoise_orm(u)


av = ModelCreateAndGetView(prefix="/auth", model=User)
app.include_router(av.get_router())

# for a in conf.apps:
#     try:
#         router = importlib.import_module(a).router
#     except AttributeError:

#         logger.warning(f'Please add from handler import router at {a}.__init__.py')
#         try:
#             router = importlib.import_module(a+'.handlers').router
#         except AttributeError:
#             logger.warning(f"router in {a} is not specified")
#             continue

#     app.include_router(router)

@app.get("/")
async def hello_world():
    return {"message": "Hello world"}