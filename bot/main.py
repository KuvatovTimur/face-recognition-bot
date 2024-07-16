import asyncio
import logging
import os
import sys

sys.path.append(os.getcwd())
from aiogram import Bot
from aiogram import Dispatcher
from aiohttp import web

from config import settings
from router import router as main_router


async def bot_polling():
    dp = Dispatcher()
    dp.include_router(main_router)
    bot = Bot(token=settings.bot.token)
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


async def handle(request):
    return web.Response(text="Bot is running")


async def main():
    loop = asyncio.get_event_loop()
    await loop.create_task(bot_polling())

    app = web.Application()
    app.router.add_get('/', handle)
    web.run_app(app, host='0.0.0.0', port=8000)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")
