from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession, AsyncAttrs, async_sessionmaker, create_async_engine
import os
from dotenv import load_dotenv
from sqlalchemy import BigInteger, Date, Time, ForeignKey, String, Boolean
import asyncpg

load_dotenv()
engine = create_async_engine(url=os.getenv('URL'))

async_session = async_sessionmaker(engine, expire_on_commit=False, future=True, class_=AsyncSession)


class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(20))
    tg_id = mapped_column(BigInteger, unique=True)

class Case(Base):
    __tablename__ = 'diary'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id'))
    date = mapped_column(Date)
    time = mapped_column(Time)
    case: Mapped[str] = mapped_column(String(120))
    success = mapped_column(Boolean)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

