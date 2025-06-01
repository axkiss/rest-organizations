from fastapi import HTTPException, Request
from sqlalchemy.exc import NoResultFound


class NotFoundHTTPException(HTTPException):
    status_code: int = 404
    detail: str = "Object does not exist"

    def __init__(self, detail: str | None = None) -> None:
        if detail:
            self.detail = detail
        super().__init__(self.status_code, self.detail, None)

    def __str__(self) -> str:
        return self.detail


async def no_result_exception_handler(request: Request, exc: NoResultFound) -> None:
    raise NotFoundHTTPException
