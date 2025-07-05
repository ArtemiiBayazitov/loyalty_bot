from gc import callbacks
from os import name
from random import setstate
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (Message, ReplyKeyboardMarkup, 
                           KeyboardButton, InlineKeyboardMarkup,
                           InlineKeyboardButton, CallbackQuery)
from aiogram.fsm.context import FSMContext

from text.text import welcome_text
from states.register_fsm import Register


router = Router()

@router.message()
async def set_phone_number(message: Message, state: FSMContext) -> None:
    await state.clear()
    contact_keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="📱 Отправить контакт", request_contact=True)]
                ],
                resize_keyboard=True,
                one_time_keyboard=True
            )
    await message.answer(
        welcome_text,
        reply_markup=contact_keyboard
    )
    await state.set_state(Register.phone_number)



@router.message(F.contact, Register.phone_number)
async def start_register(message: Message) -> None:
    register_button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Регистрация', callback_data='phone_number')]
    ])
    await message.answer(
        welcome_text,
        reply_markup=register_button
    )



# @router.callback_query(F.data == 'phone_number')
# async def get_phone_number(callback: CallbackQuery, state: FSMContext) -> None:
#     await state.clear()
#     await callback.message.delete_reply_markup()

    
#     await callback.message.answer(
#         ,
#         reply_markup=contact_keyboard)
    
#     await state.set_state(Register.phone_number)
    

# @router.message(Register.phone_number, F.contact)
# async def get_last_name(message: Message, state: FSMContext):
#     await state.update_data(phone_number=message.text)
#     await state.set_state(Register.last_name)
        



