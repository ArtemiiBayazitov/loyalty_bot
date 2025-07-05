from aiogram import Router, types
from aiogram.filters import CommandStart

from database.requests import is_auth
from handlers.register import set_phone_number
from handlers.main_menu import main_menu


router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    auth_user: bool = await is_auth(message.from_user.id)
    if auth_user:
        await main_menu(message)
    else:
        await set_phone_number(message)
        
