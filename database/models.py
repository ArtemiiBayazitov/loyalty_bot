from sqlalchemy import BigInteger, ForeignKey, Integer, String, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from datetime import datetime, date

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite')

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, index=True
        )
    phone_number: Mapped[str | None] = mapped_column(String(20), unique=True)
    username: Mapped[str | None] = mapped_column(String(32))
    full_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str | None] = mapped_column(String(50), unique=True)
    sex: Mapped[str] = mapped_column(String)
    birthday: Mapped[date] = mapped_column(Date, index=True)
    registered_at: Mapped[datetime] = mapped_column(default=datetime.now)


class LoyaltyData(Base):
    __tablename__ = 'loyalty_data'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    last_activity: Mapped[datetime | None] = mapped_column(default=None)
    barcode_path: Mapped[str | None] = mapped_column(String(255))
    barcode_num: Mapped[int | None] = mapped_column(BigInteger, unique=True)
    discount_status: Mapped[int] = mapped_column(Integer, default=0)
    session_counter: Mapped[int | None] = mapped_column(Integer, default=0)


async def async_main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

