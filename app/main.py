from fastapi import FastAPI
from sqlalchemy import text


from app.database.base import Base
from app.database.session import engine
from app.api.v1.router import router as api_router

import app.models


app = FastAPI()


@app.on_event("startup")
async def startup():

    async with engine.begin() as connection:

        await connection.run_sync(
            Base.metadata.create_all
        )



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