from app.common.exceptions import BadRequestException, UnauthorizedException


class InvalidCredentialsException(BadRequestException):
    def __init__(self) -> None:
        super().__init__(target="auth", additional_info="invalid_credentials")


class InvalidTokenException(UnauthorizedException):
    def __init__(self) -> None:
        super().__init__(target="auth")
