from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (Message, ReplyKeyboardMarkup, 
                           KeyboardButton, InlineKeyboardMarkup,
                           InlineKeyboardButton, CallbackQuery,
                           FSInputFile, InputMediaPhoto, ReplyKeyboardRemove)
from states.support_fsm import Support
from aiogram.fsm.context import FSMContext
from text.text import (gift_text, delivery_text, loyalty_text,
                       support_text, support_message_text)


router = Router()


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
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Каталог Подарков', callback_data='gifts')],
        [InlineKeyboardButton(text='Доставка', callback_data='delivery')],
        [InlineKeyboardButton(text='Сотрудничество', callback_data='work')],
        [InlineKeyboardButton(text='Правила программы лояльности', callback_data='loyalty')],
        [InlineKeyboardButton(text='Поддержка', callback_data='support')],
    ])
    await message.answer(
        text='Выберите интересующий раздел',
        reply_markup=inline_kb,
    )


@router.callback_query(F.data == 'gifts')
async def get_gifts(call: CallbackQuery) -> None:
    await call.message.answer(
        text=gift_text,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'delivery')
async def get_delivery_info(call: CallbackQuery) -> None:
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Вольсов', url='https://eda.yandex.ru/ulyanovsk/r/vol_sov?placeSlug=volsov_zhxsp')],
        [InlineKeyboardButton(text='Gonzo', url='https://eda.yandex.ru/r/gonzo')],
        [InlineKeyboardButton(text='Антресоль', url='https://antresol.drugierestorany.ru/dostavka')]
    ])
    await call.message.answer(
        delivery_text,
        reply_markup=inline_kb
    )


@router.callback_query(F.data == 'loyalty')
async def get_loyalty_info(call: CallbackQuery) -> None:
    await call.message.answer(
        text=loyalty_text,
        parse_mode='HTML'
    )


@router.message(Command('support'))
async def get_support_info_message(message: Message, state: FSMContext) -> None:
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='вопрос по карте лояльности', callback_data='loyalty_question')],
        [InlineKeyboardButton(text='вопрос по визиту или доставке в Антресоль', callback_data='antresol_question')],
        [InlineKeyboardButton(text='вопрос по визиту или доставке в Вольсов', callback_data='volsov_question')],
        [InlineKeyboardButton(text='вопрос по визиту или доставке в Gonzo', callback_data='gonzo_question')],
    ])
    await message.answer(
        text=support_text,
        reply_markup=inline_kb,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'support')
async def get_support_info_callback(call: CallbackQuery, state: FSMContext) -> None:
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='вопрос по карте лояльности', callback_data='loyalty_question')],
        [InlineKeyboardButton(text='вопрос по визиту или доставке в Антресоль', callback_data='antresol_question')],
        [InlineKeyboardButton(text='вопрос по визиту или доставке в Вольсов', callback_data='volsov_question')],
        [InlineKeyboardButton(text='вопрос по визиту или доставке в Gonzo', callback_data='gonzo_question')],
    ])
    await call.message.answer(
        text=support_text,
        reply_markup=inline_kb,
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


@router.message(F.text, Support.support_message)
async def get_support_message(message: Message, state: FSMContext) -> None:
    data = message.text
    await state.update_data(support_message=data)
    await message.answer(
        text='Ваше сообщение зарегистрировано.Скоро с Вами свяжется наш сотрудник /start'
    )
    await state.clear()
    


@router.callback_query(F.data == 'work')
async def set_work_message(call: CallbackQuery, state: FSMContext):
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Реклама и маркетинг', callback_data='marketing')],
        [InlineKeyboardButton(text='Поставки', callback_data='sales')],
        [InlineKeyboardButton(text='Инвестиции', callback_data='invest')],
        [InlineKeyboardButton(text='Вернуться в главное меню', callback_data='main_menu')],
    ])
    await call.message.answer(
        text='<b>Выберите интресующий раздел</b>👇',
        reply_markup=inline_kb,
        parse_mode='HTML'
    )


    
    