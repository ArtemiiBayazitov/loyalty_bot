from database.models import async_session
from database.models import User
from sqlalchemy import delete, select, update


async def is_auth(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(
            select(User).where(User.telegram_id == tg_id)
            )
    return bool(user)


async def save_data_on_db(fsm_data: dict) -> int:
    async with async_session() as session:
        user_data = User(
            telegram_id=fsm_data['telegram_id'],
            phone_number=fsm_data.get('phone_number'),
            username=fsm_data.get('username'),
            full_name=fsm_data.get('first_name'),
            last_name=fsm_data.get('last_name'),
            email=fsm_data.get('email'),
            sex=fsm_data.get('sex'),
            birthday=fsm_data.get('date_of_birth'),
        )
        session.add(user_data)
        await session.commit()
        return user_data.id

    
