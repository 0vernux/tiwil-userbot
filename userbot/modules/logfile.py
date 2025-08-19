"""
отправляет лог файл по команде
• .logfile
"""
from telethon import events
import os
import asyncio

# Используем переменную внутри функции, чтобы не было глобального мусора
_registered = False

async def setup(bot):
    global _registered
    if _registered:
        return  # Хендлер уже был добавлен

    @bot.client.on(events.NewMessage(pattern=r"\.logfile"))
    async def logfile_handler(event):
        log_path = "logs/bot.log"

        # Проверим до 3 раз с интервалом
        for _ in range(3):
            if os.path.exists(log_path):
                await bot.client.send_file(event.chat_id, log_path, caption="📄 Лог-файл")
                return
            await asyncio.sleep(0.5)

        await event.reply("❌ Лог-файл не найден.")

    _registered = True