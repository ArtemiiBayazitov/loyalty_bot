from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


router = Router()


@router.message(Command('main_menu'))
async def main_menu(message: Message):
    await message.answer(
        text='Это главное меню'
    )