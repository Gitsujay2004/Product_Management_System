import pytest_asyncio

from httpx import AsyncClient, ASGITransport

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from sqlalchemy.pool import NullPool

from app.main import app as fastapi_app
from app.database.base import Base
from app.database.session import get_db
from app.core.settings import settings

from app.core.security import hash_password
from app.models.user_model import User

import app.models

from app.core.rate_limiter import limiter

# ============================================================
# TEST DATABASE
# ============================================================

test_engine = create_async_engine(
    settings.TEST_DATABASE_URL,
    echo=False,
    poolclass=NullPool,
)


TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ============================================================
# TEST DATABASE FIXTURE
# ============================================================

@pytest_asyncio.fixture
async def test_database():

    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


# ============================================================
# NORMAL TEST CLIENT
# ============================================================

@pytest_asyncio.fixture
async def client(test_database):

    limiter.reset()

    async def override_get_db():
        async with TestSessionLocal() as session:
            yield session

    fastapi_app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=fastapi_app)

    async with AsyncClient(
        transport=transport,
        base_url="http://localhost"
    ) as client:
        yield client

    fastapi_app.dependency_overrides.clear()

# ============================================================
# ADMIN TEST CLIENT
# ============================================================

@pytest_asyncio.fixture
async def admin_client(client):

    # --------------------------------------------------------
    # Create admin user directly in TEST DATABASE
    # --------------------------------------------------------

    async with TestSessionLocal() as db:

        admin_user = User(
            username="pytest_admin",
            email="pytest_admin@example.com",
            password=hash_password("Test@12345"),
            role="admin",
            is_active=True
        )

        db.add(admin_user)

        await db.commit()


    # --------------------------------------------------------
    # Login admin user
    # --------------------------------------------------------

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "pytest_admin@example.com",
            "password": "Test@12345"
        }
    )

    assert login_response.status_code == 200

    login_data = login_response.json()

    access_token = login_data["access_token"]


    # --------------------------------------------------------
    # Return client + admin authorization header
    # --------------------------------------------------------

    return {
        "client": client,
        "headers": {
            "Authorization": f"Bearer {access_token}"
        }
    }