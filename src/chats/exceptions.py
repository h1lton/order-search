from fastapi import HTTPException
from starlette import status


def not_chat_exception(username):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Cannot find any entity corresponding to \"{username}\""
    )


def not_found_exception(exp):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=exp.args[0]
    )


UsernameInvalidException = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail="Some username does not correspond to r\"[a-zA-Z][\\w\\d]{3,30}[a-zA-Z\\d]\""
)
