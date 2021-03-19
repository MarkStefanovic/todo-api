import fastapi
import pydantic
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from src import service_locator, core, auth
from src.api import exceptions, response

__all__ = (
    "get_current_active_user",
    "router",
)


router = fastapi.APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


def get_current_active_user(
    token: str = fastapi.Depends(oauth2_scheme),
    token_service: auth.TokenService = fastapi.Depends(
        service_locator.default().token_service
    ),
    user_service: auth.UserService = fastapi.Depends(
        service_locator.default().user_service
    ),
) -> auth.User:
    username = token_service.username(token=token)
    if active_user := user_service.get_user(username):
        return active_user
    raise exceptions.CREDENTIALS_EXCEPTION


@router.post("/token", response_model=auth.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = fastapi.Depends(),
    user_service: auth.UserService = fastapi.Depends(
        service_locator.default().user_service
    ),
    password_hasher: auth.PasswordHashService = fastapi.Depends(
        service_locator.default().password_hasher
    ),
    token_service: auth.TokenService = fastapi.Depends(
        service_locator.default().token_service
    ),
) -> auth.Token:
    try:
        user = user_service.get_user(form_data.username)
    except core.exception.UserNotFound:
        raise exceptions.CREDENTIALS_EXCEPTION
    else:
        if password_hasher.verify(
            hashed_password=user.password_hash,
            plain_password=pydantic.SecretStr(form_data.password),
        ):
            return token_service.create({"sub": user.username})
        else:
            raise exceptions.CREDENTIALS_EXCEPTION


@router.get("/user", response_model=auth.User)
async def get_user(
    current_user: auth.User = fastapi.Depends(get_current_active_user),
) -> response.UserResponse:
    return response.UserResponse.from_domain(current_user)


@router.post("/user", response_model=auth.User, status_code=201)
async def register(
    username: str,
    email: pydantic.EmailStr,
    password: str,
    user_service: auth.UserService = fastapi.Depends(
        service_locator.default().user_service
    ),
    password_hasher: auth.PasswordHashService = fastapi.Depends(
        service_locator.default().password_hasher
    ),
) -> response.UserResponse:
    pw_hash = password_hasher.create(pydantic.SecretStr(password))
    user = user_service.create_user(
        username=username, email=email, password_hash=pw_hash
    )
    return response.UserResponse.from_domain(user)
