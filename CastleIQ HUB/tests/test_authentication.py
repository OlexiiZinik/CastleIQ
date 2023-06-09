import pytest
from httpx import AsyncClient, Headers

from api.authentication.models import User, Token, UserCredentials, UserPydantic
from api.authentication.events import *

@pytest.fixture()
def credentials():
    return UserCredentials(username="test_user", password="test_password")


@pytest.mark.anyio
async def test_get_me_unauthorized(client: AsyncClient):
    response = await client.get("/users/me")
    assert response.status_code == 401


@pytest.mark.anyio
async def test_register(client: AsyncClient, credentials: UserCredentials):
    response = await client.post("/users/register", content=credentials.json())
    assert response.status_code == 201
    created_event = UserCreatedEvent.parse_raw(response.text)
    token = created_event.token
    assert token.token_type == "Bearer"
    assert token.access_token not in [None, "", " "]
    u = await User.filter(username=credentials.username).first()
    assert u is not None
    assert u.username == credentials.username == created_event.user.username


@pytest.mark.anyio
async def test_register_already_existing(client: AsyncClient, credentials: UserCredentials):
    response = await client.post("/users/register", content=credentials.json())
    assert response.status_code == 409


@pytest.mark.anyio
async def test_login(client: AsyncClient, credentials: UserCredentials):
    response = await client.post("/users/login", content=credentials.json())
    assert response.status_code == 200
    logged_in_event = UserLoggedInEvent.parse_raw(response.text)
    token = logged_in_event.token
    assert token.token_type == "Bearer"
    assert token.access_token not in [None, "", " "]
    assert credentials.username == logged_in_event.user.username


@pytest.mark.anyio
async def test_login_with_wrong_credentials(client: AsyncClient, credentials: UserCredentials):
    credentials.password = "wrong password"
    response = await client.post("/users/login", content=credentials.json())
    assert response.status_code == 401


@pytest.mark.anyio
async def test_get_me_authorized(client: AsyncClient, credentials: UserCredentials):
    response_login = await client.post("/users/login", content=credentials.json())
    assert response_login.status_code == 200
    logged_in_event = UserLoggedInEvent.parse_raw(response_login.text)
    token = logged_in_event.token
    headers = Headers({"Authorization": f'{token.token_type} {token.access_token}'})
    response_get_me = await client.get("/users/me", headers=headers)
    assert response_get_me.status_code == 200
    get_me_event = GetMeEvent.parse_raw(response_get_me.text)
    assert get_me_event.user.username == credentials.username == logged_in_event.user.username
