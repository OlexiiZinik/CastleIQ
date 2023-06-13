import json
import httpx

from config import conf


def main():
    with httpx.Client(verify=False) as client:
        try:
            response = client.get(f"https://localhost:{conf.port}")
        except httpx.ConnectError:
            print("Запустіть CastleIQ HUB")
            return
        login = input("Введіть логін: ")
        password = input("Введіть пароль: ")
        credentials = {"username": login, "password": password}
        try:
            response = client.post(f"https://localhost:{conf.port}/users/register", content=json.dumps(credentials))
            if response.status_code == 201:
                print("Користувача створено успішно")
            elif response.status_code == 409:
                print("Користувач з таким іменем вже існує")
            elif response.status_code == 422:
                print("Не правильні дані")
        except httpx.ConnectError:
            print("Щось пішло не так")
            raise


if __name__ == "__main__":
    main()
