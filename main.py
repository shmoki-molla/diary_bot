from aiogram import Bot, Dispatcher
import os
import asyncio
from dotenv import load_dotenv
from app.handlers import router, notify
from app.database.models import async_main
import aioschedule

async def scheduler():
    aioschedule.every().day.at("9:00").do(notify)
    aioschedule.every(10).seconds.do(notify)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup():
    asyncio.create_task(scheduler())

async def main():
    await async_main()
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN_API'))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot, on_startup=on_startup)

if __name__ == '__main__':
    asyncio.run(main())