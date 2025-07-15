import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import TOKEN
from handlers import start, register, main_menu


from database.models import async_main


dp = Dispatcher()


async def set_command(bot: Bot):
    commands = [
        BotCommand(command="start", description="Старт"),
        BotCommand(command="card", description="Моя карта"),
        BotCommand(command="balance", description="Баланс"),
        BotCommand(command="support", description="Поддержка")
    ]
    await bot.set_my_commands(commands)


async def main() -> None:
    await async_main()
    bot = Bot(token=TOKEN, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML)
        )
    await set_command(bot)
    dp.include_router(start.router)
    dp.include_router(register.router)
    dp.include_router(main_menu.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

