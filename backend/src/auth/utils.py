from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

from src.config import settings


async def verify_header_api_key(api_key: str = Depends(APIKeyHeader(name="X-API-Key"))):
    if api_key != settings.api_access_key:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid API key")
