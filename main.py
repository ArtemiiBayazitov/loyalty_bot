import asyncio
from atexit import register
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import TOKEN
from handlers import start, register, main_menu


from database.models import async_main


dp = Dispatcher()


async def main() -> None:
    await async_main()
    bot = Bot(token=TOKEN, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML)
        )
    dp.include_router(start.router)
    dp.include_router(register.router)
    dp.include_router(main_menu.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

