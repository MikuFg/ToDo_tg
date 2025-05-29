from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_columnn
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db_todolist.sqlite3', echo=True)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_columnn(primary_key = True)
    tg_id = mapped_columnn(BigInteger)


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_columnn(primary_key = True)
    title: Mapped[str] = mapped_columnn(String(255))
    completed: Mapped[bool] = mapped_columnn(default = False)
    user: Mapped[int] = mapped_columnn(ForeignKey('users.id', ondelete='CASCADE'))


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
