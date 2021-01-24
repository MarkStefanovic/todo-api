__all__ = (
    "TodoApiException",
    "AuthException",
    "CredentialsException",
    "InactiveUserException",
    "InvalidConfigurationSetting",
    "UserNotFound",
)


class TodoApiException(Exception):
    def __init__(self, /, error_message: str):
        self.error_message = error_message


class AuthException(TodoApiException):
    def __init__(self, /, error_message: str) -> None:
        self.error_message = error_message


class CredentialsException(AuthException):
    ...


class InactiveUserException(AuthException):
    def __init__(self) -> None:
        super().__init__("User is not active")


class InvalidConfigurationSetting(AuthException):
    def __init__(self, setting: str, message: str) -> None:
        self.setting = setting
        super().__init__(message)


class MalformedTokenException(AuthException):
    ...


class TokenDecodeException(AuthException):
    ...


class UserNotFound(AuthException):
    ...
