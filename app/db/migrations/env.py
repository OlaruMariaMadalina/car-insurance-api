from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy import create_engine, pool
from alembic import context

from app.config import settings
from app.db.base import Base
from app.models import *

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def get_sync_url() -> str:
    """
    Returns a synchronous database URL for Alembic migrations.
    If the URL uses asyncpg, it replaces it with psycopg2 for sync operations.
    """
    url = settings.database_url
    if url.startswith("postgresql+asyncpg://"):
        url = url.replace("postgresql+asyncpg://", "postgresql+psycopg2://")
    return url

config.set_main_option("sqlalchemy.url", get_sync_url())

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=get_sync_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Run migrations in 'online' mode.

    This creates an Engine and associates a connection with the context.
    Migrations are run within a transaction.
    """
    connectable = create_engine(get_sync_url(), poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
