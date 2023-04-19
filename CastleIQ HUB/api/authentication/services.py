from core.services import ModelService
from .models import User, UserPydantic, UserInPydantic


class UserService(ModelService):
    model = User
    pydantic_model_in = UserInPydantic
    pydantic_model_out = UserPydantic
