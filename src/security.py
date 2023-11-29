from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette import status

from .config import settings

security = HTTPBearer()


def access_check(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    if settings.ACCESS_TOKEN != credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
