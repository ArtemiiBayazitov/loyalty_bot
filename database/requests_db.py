from database.models import async_session
from database.models import User, Complaint
from sqlalchemy import Select, delete, select, update
from aiogram.types import CallbackQuery, Message

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

    
async def save_complaint_on_db(*args, **kwargs) -> None:
    async with async_session() as session:
        result = await session.execute(
            Select(Complaint, User.full_name)
            .join(User, Complaint.user_id == 'User.id')
        )
        print(result)
    # async with async_session() as session:
    #     complaint = Complaint(
    #         user_id=,
    #         text=fsm_date.get('text'),
    #         id_photo=fsm_date.get('id_photo'),
    #         status='new',
    #         location=fsm_date.get('location')
    #     )
    #     session.add(complaint)
    #     await session.commit()
        return