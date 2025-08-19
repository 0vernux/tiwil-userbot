from core.bot import UserBot
import asyncio
from core.logger_mod import logger

async def main():
    bot = UserBot()  # параметры берутся внутри UserBot из ../private/config.py
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())