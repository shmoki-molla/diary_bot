from aiogram import Bot, Dispatcher
import os
import asyncio
from dotenv import load_dotenv
from app.handlers import router
from app.database.models import async_main



async def main():
    await async_main()
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN_API'))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())