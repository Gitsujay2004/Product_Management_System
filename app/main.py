from fastapi import FastAPI
from sqlalchemy import text


from app.database.base import Base
from app.database.session import engine
from app.old_approach.category import router as category_router
from app.old_approach.product import router as product_router
from app.old_approach.product_image import router as product_image_router
from app.api.v1.endpoints.user_router import router as user_router
from app.old_approach.session import router as session_router

import app.models


app = FastAPI()


@app.on_event("startup")
async def startup():

    async with engine.begin() as connection:

        await connection.run_sync(
            Base.metadata.create_all
        )


app.include_router(category_router)
app.include_router(product_router)
app.include_router(product_image_router)
app.include_router(user_router)
app.include_router(session_router)


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