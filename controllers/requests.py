from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from fastapi import status

from models.response import Res


def success_response(data):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(Res(
            status="success",
            message="Request processed successfully",
            data=data,
        )),
    )


def error_response(data):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(Res(
            status="error",
            message="Request processed failed",
            data=data,
        )),
    )


def not_found_response(data):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder(Res(
            status="error",
            message="Request processed failed",
            data=data,
        )),
    )


def bad_request_response(data):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(Res(
            status="error",
            message="Request processed failed",
            data=data,
        )),
    )


def internal_server_error_response(data):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(Res(
            status="error",
            message="Request processed failed",
            data=data,
        )),
    )


def unauthorized_response(data):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=jsonable_encoder(Res(
            status="error",
            message="Request processed failed",
            data=data,
        )),
    )


def forbidden_response(data):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=jsonable_encoder(Res(
            status="error",
            message="Request processed failed",
            data=data,
        )),
    )


def method_not_allowed_response(data):
    return JSONResponse(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        content=jsonable_encoder(Res(
            status="error",
            message="Request processed failed",
            data=data,
        )),
    )
