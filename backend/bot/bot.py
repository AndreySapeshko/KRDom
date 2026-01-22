import asyncio
import logging

from aiogram import Bot, Dispatcher

from backend.config import ENABLE_TELEGRAM, TELEGRAM_BOT_TOKEN

logger = logging.getLogger(__name__)

if ENABLE_TELEGRAM:
    bot = Bot(TELEGRAM_BOT_TOKEN)
else:
    bot = None

dp = Dispatcher()

routers = []


def setup_routers(dp: Dispatcher, routers: list):
    for router in routers:
        dp.include_router(router)


async def main():

    setup_routers(dp, routers)

    if not bot:
        print("❌ DISABLED start bot")

    if bot:
        print("🤖 Bot service started")
        try:
            await dp.start_polling(bot)
        finally:
            await bot.session.close()


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
