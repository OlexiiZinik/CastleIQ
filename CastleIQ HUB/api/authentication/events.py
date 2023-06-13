from castleiq_events import ResponseEvent, EventResult, RequestEvent
from .models import UserPydantic, Token


class InvalidTokenError(ResponseEvent):
    status_code = 401
    event_result = EventResult.ERROR
    event_name = "InvalidTokenError"
    message = "JWT не дійсний"


class TokenExpiredError(ResponseEvent):
    status_code = 401
    event_result = EventResult.ERROR
    event_name = "TokenExpiredError"
    message = "Час токену сплив"


class WrongCredentialsError(ResponseEvent):
    status_code = 401
    event_result = EventResult.ERROR
    event_name = "WrongCredentialsError"
    message = "Логін чи пароль не вірні"


class UserAlreadyExistsError(ResponseEvent):
    status_code = 409
    event_result = EventResult.ERROR
    event_name = "UserAlreadyExistsError"
    message = "Користувач з таким логіном вже існує"


class UserNotAuthorizedError(ResponseEvent):
    status_code = 401
    event_result = EventResult.ERROR
    event_name = "UserNotAuthorizedError"
    message = "Немає доступу. Користувач не авторизований"


class UserCreatedEvent(ResponseEvent):
    status_code = 201
    event_result = EventResult.SUCCESS
    event_name = "UserCreatedEvent"
    message = "Користувача створено успішно"
    user: UserPydantic
    token: Token


class UserLoggedInEvent(ResponseEvent):
    status_code = 200
    event_result = EventResult.SUCCESS
    event_name = "LoggedInEvent"
    message = "Користувач успішно увійшов"
    user: UserPydantic
    token: Token


class GetMeEvent(ResponseEvent):
    status_code = 200
    event_result = EventResult.SUCCESS
    event_name = "GetMeEvent"
    user: UserPydantic
    message = "Користувача знайдено"

