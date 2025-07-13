from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text
from expense_tracker.config import settings
import asyncpg
import asyncio
from urllib.parse import urlparse

engine = create_async_engine(settings.DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def create_database_if_not_exists():
    """create database if not exists"""
    parsed_url = urlparse(settings.DATABASE_URL.replace('postgresql+asyncpg://', 'postgresql://'))
    
    try:
        conn = await asyncpg.connect(
            host=parsed_url.hostname,
            port=parsed_url.port or 5432,
            user=parsed_url.username,
            password=parsed_url.password,
            database='postgres'
        )
        
        db_name = parsed_url.path[1:]
        result = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1",
            db_name
        )
        
        if not result:
            print(f"Creating database '{db_name}'...")
            await conn.execute(f"CREATE DATABASE {db_name}")
            print(f"✅ Database '{db_name}' created")
        else:
            print(f"✅ Database '{db_name}' already exists")
        
        await conn.close()
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        raise

async def create_tables():
    """create all tables in database"""
    from expense_tracker.models.base import Base
    from expense_tracker.models import user, balance_change, expense_category, income_category
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("✅ All tables created")

async def init_database():
    """initialize database: create it if not exists and create tables"""
    await create_database_if_not_exists()
    # await create_tables()
