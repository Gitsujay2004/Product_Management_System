from fastapi import FastAPI,Request
from sqlalchemy import text


# from app.database.base import Base
from app.database.session import engine
from app.api.v1.router import router as api_router

import app.models

from fastapi.responses import JSONResponse
from app.exceptions.custom_exceptions import AppException
from fastapi.exceptions import RequestValidationError

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.middleware.security_headers import SecurityHeadersMiddleware

from sqlalchemy.exc import IntegrityError

#Error Logging

import logging

from app.core.logging import setup_logging






app = FastAPI()


#Error Logging

setup_logging()

logger = logging.getLogger(__name__)



app.add_middleware(
    SecurityHeadersMiddleware
)


#Trust host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "localhost",
        "127.0.0.1"
    ]
)

#CORs configuration 

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # don't use allow_origins=["*"] 
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


#exception handling
@app.exception_handler(AppException)
async def app_exception_handler(
    request: Request,
    exc: AppException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
            "error_code": exc.error_code,
            "details": None
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation error",
            "error_code": "VALIDATION_ERROR",
            "details": exc.errors()
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    logger.exception(
        "Unhandled exception: %s %s",
        request.method,
        request.url.path
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "error_code": "INTERNAL_SERVER_ERROR",
            "details": None
        }
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(
    request: Request,
    exc: IntegrityError
):
    error_message = str(exc.orig).lower()

    if "unique" in error_message:
        message = "A record with the same unique value already exists"
        error_code = "DUPLICATE_VALUE"

    elif "foreign key" in error_message:
        message = "Referenced resource does not exist"
        error_code = "INVALID_REFERENCE"

    else:
        message = "Database constraint violation"
        error_code = "DATABASE_CONSTRAINT_ERROR"

    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": message,
            "error_code": error_code,
            "details": None
        }
    )


# @app.on_event("startup")
# async def startup():

#     async with engine.begin() as connection:

#         await connection.run_sync(
#             Base.metadata.create_all
#         )



app.include_router(
    api_router,
    prefix="/api/v1"
)


@app.get("/")
async def home():

    return {
        "message": "Product Management API is running"
    }


@app.get("/database-test")
async def database_test():

    async with engine.connect() as connection:

        result = await connection.execute(
            text("SELECT 1")
        )

        return {
            "database": "PostgreSQL connected successfully",
            "result": result.scalar()
        }