from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.exceptions import IntegrityError

from .models import UserInPydantic, UserPydantic, User, Token, UserCredentials
from .services import UserService
from .events import *
from logger import logger

router = APIRouter(prefix="/users", tags=["Authentication"])
service = UserService()


# @router.get("/", response_model=list[UserPydantic])
# async def all_users():
#     return await service.api_get_all()


@router.post("/register", status_code=201, response_model=UserCreatedEvent)
async def register_user(credentials: UserCredentials):
    return await service.register_user(credentials)


@router.post("/login", response_model=UserLoggedInEvent)
async def login_user(user: UserCredentials):
    return await service.login(user)


@router.post("/loginform", response_model=Token)
async def login_form(token=Depends(service.login_form)):
    return token


@router.get("/me", response_model=UserPydantic)
async def get_me(user: User = Depends(service.get_current_user)):
    return user
