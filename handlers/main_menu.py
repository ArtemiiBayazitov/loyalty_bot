from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (Message, ReplyKeyboardMarkup, 
                           KeyboardButton, InlineKeyboardMarkup,
                           InlineKeyboardButton, CallbackQuery,
                           FSInputFile, InputMediaPhoto, ReplyKeyboardRemove)
from states.support_fsm import Support
from aiogram.fsm.context import FSMContext
from text.text import *
from keyboards import *
from database.requests_db import save_complaint_on_db

router = Router()


@router.callback_query(F.data == 'start')
@router.message(Command('main_menu'))
async def main_menu(update: Message | CallbackQuery) -> None:
    if isinstance(update, CallbackQuery):
        message = update.message
    else:
        message = update
    reply_kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Баланс и уровень')], 
        [KeyboardButton(text='Показать карту')],
        [KeyboardButton(text='Дополнительно')],
        
        ],
        resize_keyboard=True,
        )
    await message.answer(
        text='Выберите пункт меню👇',
        reply_markup=reply_kb,
    )


@router.message(F.text == 'Показать карту')
@router.message(Command('card'))
async def get_card(message: Message) -> None:
    barcode_image = FSInputFile('barcodes/images/01234567.jpg')
    barcode_num = '0123-4567'
    try:
        await message.answer_photo(
            photo=barcode_image,
            caption=f'<b>Номер вашей карты: {barcode_num}</b>',
            parse_mode='HTML'
        )
    except Exception:
        await message.answer(
            text='Повторите запрос чуть позже'
        )


@router.message(F.text == 'Баланс и уровень')
@router.message(Command('balance'))
async def get_balance(message: Message) -> None:
    balance = 150
    level = 'bronze'
    await message.answer(
        text=f'Ваш баланс: {balance} бонусов\nУровень: {level}'
    )


@router.message(F.text == 'Дополнительно')
async def more_options(message: Message) -> None:

    await message.answer(
        text='Выберите интересующий раздел',
        reply_markup=more_inline_kb,
    )


@router.callback_query(F.data == 'gifts')
async def get_gifts(call: CallbackQuery) -> None:
    await call.message.answer(
        text=gift_text,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'delivery')
async def get_delivery_info(call: CallbackQuery) -> None:
    await call.message.answer(
        delivery_text,
        reply_markup=delivery_inline_kb,
    )


@router.callback_query(F.data == 'loyalty')
async def get_loyalty_info(call: CallbackQuery) -> None:
    await call.message.answer(
        text=loyalty_text,
        parse_mode='HTML'
    )


@router.message(Command('support'))
async def get_support_info_message(message: Message, state: FSMContext) -> None:
    await message.answer(
        text=support_text,
        reply_markup=support_inline_kb,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'support')
async def get_support_info_callback(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(
        text=support_text,
        reply_markup=support_inline_kb,
        parse_mode='HTML'
    )

support_callback = ['loyalty_question', 'antresol_question', 'volsov_question', 'gonzo_question']


@router.callback_query(F.data.in_(support_callback))
async def set_support_message(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    await state.set_state(Support.support_message)
    await call.message.answer(
        text=support_message_text,
        reply_markup=ReplyKeyboardRemove()
    )


@router.message((F.text | F.photo), Support.support_message)
async def get_support_message(message: Message, state: FSMContext) -> None:
    # photo_id = message.photo[-1].file_id if message.photo else None
    
    # await save_complaint_on_db(message.from_user.id, message.text, photo_id, )

    await message.answer(
        text='Ваше сообщение зарегистрировано.Скоро с Вами свяжется наш сотрудник',
        reply_markup=back_inline_button,
    )
    await state.clear()
    

@router.callback_query(F.data == 'work')
async def set_work_message(call: CallbackQuery, state: FSMContext):
    await call.message.answer(
        text='<b>Выберите интресующий раздел</b>👇',
        reply_markup=work_inline_kb,
        parse_mode='HTML',
    )


    
    