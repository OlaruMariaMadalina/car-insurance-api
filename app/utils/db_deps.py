from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.engine import SessionLocal

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function for FastAPI routes to provide an asynchronous database session.

    Yields:
        AsyncSession: An active SQLAlchemy asynchronous session.

    Usage:
        Use as a dependency in FastAPI endpoints to access the database.
    """
    async with SessionLocal() as session:
        yield session