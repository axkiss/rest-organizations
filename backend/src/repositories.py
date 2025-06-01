from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession


class IBaseRepository(ABC):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
