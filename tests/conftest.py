import asyncio
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from core.db.models import Base
from modules.auth.service import AuthService
from modules.user.models import User
from modules.user.repository import UserRepository
from modules.user.service import UserService

# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create async engine for tests
engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
async def async_engine():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
async def async_session(async_engine) -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


@pytest.fixture(autouse=True)
async def setup_database() -> AsyncGenerator[None, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


@pytest.fixture
def client() -> Generator:
    from core.server import create_fastapi_app

    app = create_fastapi_app()
    with TestClient(app) as c:
        yield c


@pytest.fixture
def user_repository(db_session: AsyncSession) -> UserRepository:
    return UserRepository(db_session)


@pytest.fixture
def user_service(user_repository: UserRepository) -> UserService:
    return UserService(user_repository)


@pytest.fixture
def auth_service(user_service: UserService) -> AuthService:
    return AuthService(user_service)


@pytest.fixture
async def test_user(db_session: AsyncSession):
    """Create a test user and return it"""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="$2b$12$FJ71jLDdFenwvXEvqDqu1uFeP7ZmnPGeXLiy6JT0OJvsUwgGpPCLC",  # "mypassword123"
        name="Test",
        last_name="User",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    yield user
    # Cleanup
    await db_session.delete(user)
    await db_session.commit()
