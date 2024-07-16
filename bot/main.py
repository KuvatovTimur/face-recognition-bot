import asyncio
import logging
import os
import sys
from aiohttp import web


sys.path.append(os.getcwd())
from aiogram import Bot
from aiogram import Dispatcher

from config import settings
from router import router as main_router


async def bot_polling():
    dp = Dispatcher()
    dp.include_router(main_router)
    bot = Bot(token=settings.bot.token)
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


async def main():
    dp = Dispatcher()
    dp.include_router(main_router)
    bot = Bot(
        token=settings.bot.token,
    )
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

    loop = asyncio.get_event_loop()
    await loop.create_task(bot_polling())

    app = web.Application()
    port = int(os.environ.get('PORT', 10000))
    web.run_app(app, host='0.0.0.0', port=port)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")
