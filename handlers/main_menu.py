from operator import call
import os
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (Message, ReplyKeyboardMarkup, 
                           KeyboardButton, InlineKeyboardMarkup,
                           InlineKeyboardButton, CallbackQuery,
                           FSInputFile, InputMediaPhoto)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from states.register_fsm import MainMenu, Register
from aiogram.fsm.context import FSMContext
from text.text import gift_text, delivery_text, loyalty_text


router = Router()


@router.message(Command('main_menu'))
async def main_menu(update: Message | CallbackQuery) -> None:
    if isinstance(update, CallbackQuery):
        message = update.message
    else:
        message = update
    reply_kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Баланс и\nуровень')], 
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
async def get_card(message: Message) -> None:
    barcode_image = FSInputFile('barcodes/images/01234567.jpg')
    barcode_num = '0123-4567'
    try:
        await message.answer_photo(
            photo=barcode_image,
            caption=f'<b>Номер вашей карты: {barcode_num}</b>',
            parse_mode='HTML'
        )
    except TelegramBadRequest as e:
        await message.answer(
            text='Повторите запрос чуть позже'
        )


@router.message(F.text == 'Баланс и\nуровень')
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