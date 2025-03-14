from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize the database engine and create tables
    engine, session_local = init_db()
    app.state.session_local = session_local
    app.state.engine = engine

    # Now we use alembic for database migration
    # # Create tables automatically
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.reflect)  # Load existing schema
    #     await conn.run_sync(Base.metadata.create_all)  # Apply changes

    # # Optionally, seed initial data
    # await seed_data(engine)

    # Yield control back to FastAPI (app is running)
    yield

    # Shutdown: Clean up, if necessary (e.g., close engine)
    await engine.dispose()
