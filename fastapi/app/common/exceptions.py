from enum import Enum
from typing import Optional

from fastapi import status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ErrorEvents(Enum):
    NOT_FOUND: str = "not_found"
    BAD_REQUEST: str = "invalid"
    UNAUTHORIZED: str = "unauthorized"
    CONFLICT: str = "conflict"
    FORBIDDEN: str = "forbidden"


def get_error_message(
    target: str, event: ErrorEvents, additional_info: Optional[str] = None
) -> str:
    return (
        f"{target}.{event.value}"
        if additional_info is None
        else f"{target}.{event.value}.{additional_info}"
    )


class CommonDetailedException(Exception):
    # pylint: disable-next=too-many-arguments
    def __init__(
        self,
        event: ErrorEvents,
        status_code: int,
        target: str,
        ids: Optional[list[int]] = None,
        additional_info: Optional[str] = None,
    ):
        self.status_code = status_code
        self.message = get_error_message(target, event, additional_info)
        self.ids = ids


class CommonError(BaseModel):
    message: str
    ids: Optional[list[int]]


async def common_error_handler(
    _: Request, exc: CommonDetailedException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "ids": exc.ids},
    )


class NotFoundException(CommonDetailedException):
    def __init__(self, target: str, ids: Optional[list[int]] = None):
        super().__init__(
            event=ErrorEvents.NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
            target=target,
            ids=ids,
        )


class BadRequestException(CommonDetailedException):
    def __init__(
        self,
        target: str,
        ids: Optional[list[int]] = None,
        additional_info: Optional[str] = None,
    ):
        super().__init__(
            event=ErrorEvents.BAD_REQUEST,
            status_code=status.HTTP_400_BAD_REQUEST,
            target=target,
            ids=ids,
            additional_info=additional_info,
        )


class UnauthorizedException(CommonDetailedException):
    def __init__(
        self,
        target: str,
        ids: Optional[list[int]] = None,
        additional_info: Optional[str] = None,
    ):
        super().__init__(
            event=ErrorEvents.UNAUTHORIZED,
            status_code=status.HTTP_401_UNAUTHORIZED,
            target=target,
            ids=ids,
            additional_info=additional_info,
        )


class ConflictException(CommonDetailedException):
    def __init__(
        self,
        target: str,
        additional_info: Optional[str] = None,
    ):
        super().__init__(
            event=ErrorEvents.CONFLICT,
            status_code=status.HTTP_409_CONFLICT,
            target=target,
            additional_info=additional_info,
        )


class ForbiddenException(CommonDetailedException):
    def __init__(
        self,
        target: str,
    ):
        super().__init__(
            event=ErrorEvents.FORBIDDEN,
            status_code=status.HTTP_403_FORBIDDEN,
            target=target,
        )
