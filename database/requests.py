from database.models import async_session
from database.models import User
from sqlalchemy import delete, select, update


async def is_auth(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(
            select(User).where(User.telegram_id == tg_id)
            )
    return True if user else False