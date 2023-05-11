from core.events.events import Event, EventResult
from .models import UserPydantic, Token


class InvalidTokenError(Event):
    status_code = 401
    event_result = EventResult.ERROR
    event_name = "InvalidTokenError"
    message = "JWT не дійсний"


class TokenExpiredError(Event):
    status_code = 401
    event_result = EventResult.ERROR
    event_name = "TokenExpiredError"
    message = "Час токену сплив"


class WrongCredentialsError(Event):
    status_code = 401
    event_result = EventResult.ERROR
    event_name = "WrongCredentialsError"
    message = "Логін чи пароль не вірні"


class UserAlreadyExistsError(Event):
    status_code = 409
    event_result = EventResult.ERROR
    event_name = "UserAlreadyExistsError"
    message = "Користувач з таким логіном вже існує"


class UserNotAuthorizedError(Event):
    status_code = 401
    event_result = EventResult.ERROR
    event_name = "UserNotAuthorizedError"
    message = "Немає доступу. Користувач не авторизований"


class UserCreatedEvent(Event):
    status_code = 201
    event_result = EventResult.SUCCESS
    event_name = "UserCreatedEvent"
    message = "Користувача створено успішно"
    user: UserPydantic
    token: Token


class UserLoggedInEvent(Event):
    status_code = 200
    event_result = EventResult.SUCCESS
    event_name = "LoggedInEvent"
    message = "Користувач успішно увійшов"
    user: UserPydantic
    token: Token
