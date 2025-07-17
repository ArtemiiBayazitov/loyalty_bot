from urllib.parse import urldefrag
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

more_inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Каталог Подарков', callback_data='gifts')],
        [InlineKeyboardButton(text='Доставка', callback_data='delivery')],
        [InlineKeyboardButton(text='Сотрудничество', callback_data='work')],
        [InlineKeyboardButton(text='Правила программы лояльности', callback_data='loyalty')],
        [InlineKeyboardButton(text='Поддержка', callback_data='support')],
    ])

delivery_inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Вольсов', url='https://eda.yandex.ru/ulyanovsk/r/vol_sov?placeSlug=volsov_zhxsp')],
        [InlineKeyboardButton(text='Gonzo', url='https://eda.yandex.ru/r/gonzo')],
        [InlineKeyboardButton(text='Антресоль', url='https://antresol.drugierestorany.ru/dostavka')]
    ])

support_inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='вопрос по карте лояльности', callback_data='loyalty_question')],
        [InlineKeyboardButton(text='вопрос по визиту или доставке в Антресоль', callback_data='antresol_question')],
        [InlineKeyboardButton(text='вопрос по визиту или доставке в Вольсов', callback_data='volsov_question')],
        [InlineKeyboardButton(text='вопрос по визиту или доставке в Gonzo', callback_data='gonzo_question')],
    ])

work_inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Реклама и маркетинг', callback_data='marketing')],
        [InlineKeyboardButton(text='Поставки', callback_data='sales')],
        [InlineKeyboardButton(text='Инвестиции', callback_data='invest')],
        [InlineKeyboardButton(text='Вернуться в главное меню', callback_data='main_menu')],
    ])

back_inline_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вернуться в начало', callback_data='start')]
])

catalog_inlint_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Каталог подарков', url='https://gifts.drugierestorany.ru/')]
])