import asyncio
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool  # <--- sync
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

from expense_tracker.models.base import Base
from expense_tracker.models import user  # обязательно

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# 💡 Два движка
ASYNC_DB_URL = config.get_main_option("sqlalchemy.url")
SYNC_DB_URL = ASYNC_DB_URL.replace("asyncpg", "psycopg2")

# Используется для autogenerate
def run_migrations_offline():
    context.configure(
        url=SYNC_DB_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

# Используется для `upgrade`
def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    connectable = create_async_engine(ASYNC_DB_URL, echo=True)
    async with connectable.begin() as conn:
        await conn.run_sync(do_run_migrations)

def run_migrations_online():
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_async_migrations())

run_migrations_online()
