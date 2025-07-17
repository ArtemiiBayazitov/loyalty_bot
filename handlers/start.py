from aiogram import Router
from aiogram.filters import CommandStart

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.requests_db import is_auth
from handlers.register import set_phone_number
from handlers.main_menu import main_menu
from states.register_fsm import Register


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    auth_user: bool = await is_auth(message.from_user.id)
    # auth_user = True
    if auth_user:
        await main_menu(message)
    else:
        await state.set_state(Register.phone_number)
        await set_phone_number(message, state)
         

