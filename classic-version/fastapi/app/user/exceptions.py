from app.common.exceptions import BadRequestException, ConflictException


class EmailAlreadyRegisteredException(ConflictException):
    def __init__(self) -> None:
        super().__init__(target="user", additional_info="email_already_registered")


class PasswordNotStrongException(BadRequestException):
    def __init__(self) -> None:
        super().__init__(target="auth", additional_info="password_not_strong")
