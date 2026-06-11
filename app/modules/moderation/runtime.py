import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.modules.moderation.handlers import router as moderation_router


load_dotenv()


async def main():
    bot_token = os.getenv("BOT_TOKEN")

    if not bot_token:
        raise RuntimeError("BOT_TOKEN not found")

    bot = Bot(token=bot_token)
    dp = Dispatcher()

    dp.include_router(moderation_router)

    print("MODERATION RUNTIME STARTED")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())