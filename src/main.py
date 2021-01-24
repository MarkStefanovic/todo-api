import typing

import pydantic
import uvicorn
import fastapi
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.core import domain
from src.service_locator import services

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = fastapi.FastAPI()

_CREDENTIALS_EXCEPTION = fastapi.HTTPException(
    status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_active_user(token: str = fastapi.Depends(oauth2_scheme)) -> domain.User:
    username = services.jwt_adapter.username(token=token)
    if user := services.user_service.get_user(username):
        return user
    raise _CREDENTIALS_EXCEPTION


@app.post("/token", response_model=domain.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = fastapi.Depends(),
) -> domain.Token:
    if user := services.user_service.get_user(form_data.username):
        if services.password_hasher.verify(
            hashed_password=user.password_hash,
            plain_password=pydantic.SecretStr(form_data.password),
        ):
            return services.jwt_adapter.create({"sub": user.username})

    raise _CREDENTIALS_EXCEPTION


@app.get("/users/me/", response_model=domain.User)
async def read_users_me(
    current_user: domain.User = fastapi.Depends(get_current_active_user),
) -> domain.User:
    print(f"{current_user=}")
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: domain.User = fastapi.Depends(get_current_active_user),
) -> typing.List[typing.Dict[str, str]]:
    return [{"item_id": "Foo", "owner": current_user.username}]


if __name__ == "__main__":
    import webbrowser
    webbrowser.open("http://localhost:8000/docs")

    import dotenv
    dotenv.load_dotenv(dotenv.find_dotenv())

    uvicorn.run(app, host="0.0.0.0", port=8000)
