from fastapi import APIRouter, HTTPException, status
from tortoise.exceptions import IntegrityError

from .models import UserInPydantic, UserPydantic
from .services import UserService
from logger import logger


router = APIRouter(prefix="/users", tags=["Authentication"])
service = UserService()


@router.get("/", response_model=list[UserPydantic])
async def all_users():
    return await service.api_get_all()


@router.post("/create", response_model=UserPydantic)
async def create_user(user: UserInPydantic):
    try:
        return await service.api_create_object(user)
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User with username '
                                                                         f'{user.username} already exists')
