import asyncio
import handlers
import callbacks
from config import Config
from aiogram import Bot, Dispatcher

async def main():

    config: Config = handlers.config
    
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    dp.include_router(handlers.router)
    dp.include_router(callbacks.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
