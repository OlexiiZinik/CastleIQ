from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import status
from tortoise.exceptions import IntegrityError

from core.services import ModelService
from .models import User, UserPydantic, UserInPydantic, Token, UserCredentials
from config import conf
from .events import *

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/loginform", auto_error=False)


class UserService(ModelService):
    model = User
    pydantic_model_in = UserInPydantic
    pydantic_model_out = UserPydantic

    def __init__(self):
        super().__init__()

    async def get_user_by_username(self, username: str) -> User:
        return await self.model.filter(username=username).first()

    def encode_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=conf.token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, conf.secret_key, algorithm=conf.algorithm)
        return encoded_jwt

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, conf.secret_key, algorithms=conf.algorithm)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            TokenExpiredError().fire()
        except jwt.JWTError as e:
            InvalidTokenError().fire()

    async def register_user(self, user: UserCredentials) -> UserCreatedEvent:
        try:
            pyd = UserInPydantic(username=user.username, hashed_password=pwd_context.hash(user.password))
            u = await self.api_create_object(pyd)
        except IntegrityError as e:
            UserAlreadyExistsError().fire()
        token = self.encode_token({"sub": getattr(u, "username", None)})
        return UserCreatedEvent(user=u, token=Token(access_token=token, token_type="Bearer"))

    async def login(self, credentials: UserCredentials) -> UserLoggedInEvent:
        print(credentials)
        u = await self.get_user_by_username(credentials.username)
        if (not u) or (not pwd_context.verify(credentials.password, u.hashed_password)):
            WrongCredentialsError().fire()

        token = self.encode_token({"sub": u.username})
        return UserLoggedInEvent(token=Token(access_token=token, token_type="Bearer"), user=u)

    async def login_form(self, credentials: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)):
        uc = UserCredentials(username=credentials.username, password=credentials.password)
        logged_in_event = await self.login(uc)
        return logged_in_event.token

    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> User:
        if token is None:
            UserNotAuthorizedError().fire()

        username: str = self.decode_token(token)
        if username is None:
            WrongCredentialsError().fire()

        user = await self.get_user_by_username(username)
        if user is None:
            WrongCredentialsError().fire()
        return user
