from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (Message, ReplyKeyboardMarkup, 
                           KeyboardButton, InlineKeyboardMarkup,
                           InlineKeyboardButton, CallbackQuery,
                           FSInputFile, InputMediaPhoto, ReplyKeyboardRemove)
from states.support_fsm import Support
from aiogram.fsm.context import FSMContext
from states.work_fsm import WorkState
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
async def set_work_callback(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(
        text=work_start_text,
        reply_markup=work_inline_kb,
        parse_mode='HTML',
    )
    await state.set_state(WorkState.lesson)


work_set = {'marketing', 'sales', 'invest'}


@router.callback_query(F.data.in_(work_set), WorkState.lesson)
async def work_contact_callback(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await state.update_data(lesson=call.data)
    print(call.data)
    await call.message.answer(
        text=work_company_text,
        parse_mode='HTML',
    )
    await state.set_state(WorkState.company)


@router.message(F.text, WorkState.company)
async def work_company_message(message: Message, state: FSMContext) -> None:
    await state.update_data(company=message.text)
    print(message.text)
    await message.answer(
        text=work_service_text,
        parse_mode='HTML',
    )
    await state.set_state(WorkState.description)


@router.message(F.text, WorkState.description)
async def work_description_message(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    print(message.text)
    await message.answer(
        text=work_offer_text,
        reply_markup=offer_inline_kb,
        parse_mode='HTML',
    )
    await state.set_state(WorkState.offer)


@router.message(F.text, WorkState.offer)
async def work_offer_message(message: Message, state: FSMContext) -> None:
    await state.update_data(offer=message.text)
    print(message.text)
    await message.answer(
        text=work_contact_text,
        parse_mode='HTML',
    )
    await state.set_state(WorkState.contact)


@router.message(F.text, WorkState.contact)
async def work_contact_message(message: Message, state: FSMContext) -> None:
    await state.update_data(contact=message.text)
    print(message.text)
    await message.answer(
        text=work_message_reg,
        parse_mode='HTML',
    )
    # data = await state.get_data()
    # await message.answer(
    #     text=f'Вот содержимое обращения: {data}'
    # )
    await state.clear()






    
    