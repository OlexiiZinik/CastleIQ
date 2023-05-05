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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/loginform")


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
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.JWTError as e:
            raise HTTPException(status_code=401, detail='Invalid token')

    async def register_user(self, user: UserCredentials) -> Token:
        try:
            pyd = UserInPydantic(username=user.username, hashed_password=pwd_context.hash(user.password))
            u = await self.api_create_object(pyd)
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User with username '
                                                                             f'{user.username} already exists')
        token = self.encode_token({"sub": getattr(u, "username", None)})
        return Token(access_token=token, token_type="Bearer")

    async def login(self, credentials: UserCredentials) -> Token:
        u = await self.get_user_by_username(credentials.username)
        if (not u) or (not pwd_context.verify(credentials.password, u.hashed_password)):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Invalid credentials')

        token = self.encode_token({"sub": u.username})

        return Token(access_token=token, token_type="Bearer")

    async def login_form(self, credentials: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)):
        uc = UserCredentials(username=credentials.username, password=credentials.password)
        return await self.login(uc)

    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        # payload = jwt.decode(token, conf.secret_key, algorithms=[conf.algorythm])
        username: str = self.decode_token(token)
        if username is None:
            raise credentials_exception

        user = await self.get_user_by_username(username)
        if user is None:
            raise credentials_exception
        return user

