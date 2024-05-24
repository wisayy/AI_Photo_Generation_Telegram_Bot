

import asyncio
import logging
import os
import signal
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from db.models import User
from tortoise import Tortoise
from config_reader import config
from bot.handlers.router import router
from bot.handlers.callback import router as callback_router
from bot.handlers.generate_image import router1
from bot.handlers.payment import router_payment

logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('aiogram').setLevel(logging.WARNING)

db_url = config.DB_URL.get_secret_value()   

async def on_startup():
    await Tortoise.init(
        db_url=db_url,
        modules={"models": ['db.models.user']}
    )
    await Tortoise.generate_schemas()
    print("БД сделана")



async def main():
    bot = Bot(
        config.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(router1)
    dp.include_router(callback_router)
    dp.include_router(router_payment)



    await bot.delete_webhook(True)
    await on_startup()
    await dp.start_polling(bot)

if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO)
    #print("bot started")
    asyncio.run(main())