from email import message
import re
from aiogram import F, Router
from aiogram.types import (Message, ReplyKeyboardMarkup, 
                           KeyboardButton, InlineKeyboardMarkup,
                           InlineKeyboardButton, CallbackQuery)
from aiogram.fsm.context import FSMContext

from handlers import main_menu
from text.text import *
from states.register_fsm import Register, MainMenu
from validators.valid import is_valid_phone, is_valid_birthday
from datetime import datetime
from handlers.main_menu import main_menu
from database.requests_db import save_data_on_db


router = Router()

@router.message(Register.start)
@router.callback_query(F.data == 'again', Register.check_data)
async def set_phone_number(update: Message | CallbackQuery, state: FSMContext) -> None:
    if isinstance(update, CallbackQuery):
        message = update.message
    else:
        message = update
    await state.clear()
    contact_keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="📱 Отправить контакт", request_contact=True)]
                ],
                resize_keyboard=True,
                one_time_keyboard=True
            )
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
                                     [InlineKeyboardButton(text='Подробнее', url='https://goo.su/4wb19P')]
                                     ])
    await message.answer(
        welcome_text,
        reply_markup=inline_kb
    )
    await message.answer(
        text=phone_text,
        reply_markup=contact_keyboard
    )
    await state.set_state(Register.phone_number)


@router.message(F.contact | F.text, Register.phone_number)
async def phone_validator(message: Message, state: FSMContext) -> None:
    if message.contact:
        phone = message.contact.phone_number
    elif is_valid_phone(message.text) is True:
        phone = message.text
    else:
        phone = is_valid_phone(message.text)
        if not phone:
            await message.answer(
                text=error_text
            )
            return        
    await state.update_data(phone_number=phone)
    await message.answer(
        text=first_name_text,
        parse_mode='HTML'
    )
    await state.set_state(Register.first_name)


@router.message(F.text, Register.first_name)
async def set_first_name(message: Message, state: FSMContext) -> None:
    if message.text.isalpha():
        name = message.text
    else:
        await message.answer(
                text=error_text
            )
        return
    await state.update_data(first_name=name) 
    data = await state.get_data()
    await message.answer(
        text=last_name_text.format(**data),
        parse_mode='HTML'
    )
    await state.set_state(Register.last_name)


@router.message(F.text, Register.last_name)
async def set_last_name(message: Message, state: FSMContext) -> None:
    if message.text.isalpha():
        name = message.text
    else:
        await message.answer(
                text=error_text
            )
        return 
    await state.update_data(last_name=name)
    await message.answer(
        text=email_text,
        parse_mode='HTML'
    )
    await state.set_state(Register.email)
    


@router.message(F.text, Register.email)
async def set_email(message: Message, state: FSMContext) -> None:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    email_valid = bool(re.fullmatch(pattern, message.text))
    if email_valid:
        email = message.text
    else:
        await message.answer(
                text=error_text
            )
        return
    await state.update_data(email=email)
    await message.answer(
        text=birthday_text,
        parse_mode='HTML'
    )
    await state.set_state(Register.date_of_birth)


@router.message(F.text, Register.date_of_birth)
async def set_birthday(message: Message, state: FSMContext) -> None:
    is_valid = is_valid_birthday(message.text)
    if is_valid:
        birthday = datetime.strptime(message.text, "%d.%m.%Y").date()
    else:
        await message.answer(
                text=error_text
            )
        return
    await state.update_data(date_of_birth=birthday)
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Мужской', callback_data='male')],
        [InlineKeyboardButton(text='Женский', callback_data='female')]
    ])
    await message.answer(
        text=sex_text,
        reply_markup=inline_kb,
        parse_mode='HTML'
    )
    await state.set_state(Register.sex)
    print(await state.get_data())


@router.callback_query(F.data.in_(['male', 'female']), Register.sex)
async def set_sex(call: CallbackQuery, state: FSMContext):
    pattern = {'male': 'Мужской', 'female': 'Женский'}
    if call.data in pattern:
        sex = call.data
    else:
        await call.answer(
                text=error_text
            )
        return
    await state.update_data(sex=pattern[sex])

    user_data = await state.get_data()

    check_text = f'''
    <b>Проверьте пожалуйста данные</b>\n
    <b>Имя: {user_data["first_name"]}</b>\n
    <b>Фамилия: {user_data["last_name"]}</b>\n
    <b>Номер телефона: {user_data["phone_number"]}</b>\n
    <b>Дата рождения: {user_data["date_of_birth"]}</b>\n
    <b>Email: {user_data["email"]}</b>\n
    <b>Пол: {user_data["sex"]}</b>\n
    '''

    inline_kb = InlineKeyboardMarkup(inline_keyboard=
                                     [
                                        [InlineKeyboardButton(text='Все верно', callback_data='ok')],
                                        [InlineKeyboardButton(text='Начать сначала', callback_data='again')]
                                     ])

    await call.message.answer(
        text=check_text,
        reply_markup=inline_kb,
        parse_mode='HTML'
    )
    await state.set_state(Register.check_data)


@router.callback_query(F.data.in_({'ok', 'again'}), Register.check_data)
async def final(call: CallbackQuery, state: FSMContext) -> None:
    if call.data == 'again':
        await state.set_state(Register.start)
    else:
        tg_data_dict = {
            'telegram_id': call.from_user.id,
            'username': call.from_user.username
        }
        user_data = await state.get_data()
        user_data.update(tg_data_dict)
        print(user_data)
        await save_data_on_db(user_data)
        await call.message.answer(
            text=complete_registration_text.format(**user_data),
        )
        await state.clear()
        await state.set_state(MainMenu.main_menu)
        await main_menu(call)









    









        



