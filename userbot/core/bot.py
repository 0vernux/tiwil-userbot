import os
import sys
import json
import asyncio
from pathlib import Path
from telethon import TelegramClient, events, Button
from core.module_manager import ModuleManager
from core.logger_mod import logger


PRIVATE_PATH = Path(__file__).resolve().parent.parent / "private"
sys.path.insert(0, str(PRIVATE_PATH))


sys.path.append(str(Path(__file__).resolve().parent.parent.parent / "private"))
import config

class UserBot:
    def __init__(self):
        session_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../private", config.SESSION_NAME))
        self.client = TelegramClient(session_path, config.API_ID, config.API_HASH)
        self.module_manager = ModuleManager(self)
        self.modules = {}
        self.owner_id = config.OWNER_ID

    async def restart(self, event=None):
        if event:
            try:
                await event.edit("🔄 Перезапускаюсь...")

                # Сохраняем ID сообщения и чат ID
                with open("restart_info.json", "w") as f:
                    json.dump({
                        "chat_id": event.chat_id,
                        "msg_id": event.id
                    }, f)
            except Exception as e:
                logger.error(f"Не удалось сохранить restart_info: {e}")

        os.system(f"nohup python3 main.py > /dev/null 2>&1 &")

        if self.client.is_connected():
            await self.client.disconnect()
        os._exit(0)

    async def notify_restart(self):
        """После рестарта заменяет сообщение на '✅ Успешно перезапущен!' или показывает ошибку"""
        try:
            if os.path.exists("restart_info.json"):
                with open("restart_info.json", "r") as f:
                    data = json.load(f)

                msg = await self.client.get_messages(data["chat_id"], ids=data["msg_id"])
                await msg.edit("✅ Успешно перезапущен!")
                os.remove("restart_info.json")
        except Exception as e:
            logger.error(f"Не удалось обновить сообщение о перезапуске: {e}")
            try:
                # Отправляем кнопку, если сообщение нельзя редактировать
                await self.client.send_message(
                    data["chat_id"],
                    "❌ Не удалось перезапустить бот.",
                    buttons=[Button.inline("📄 Показать лог", b"show_log")]
                )
            except Exception as e2:
                logger.error(f"И не удалось отправить сообщение об ошибке: {e2}")

    async def setup_handlers(self):
        """Регистрация встроенных команд"""

        @self.client.on(events.NewMessage(pattern=r"\.start"))
        async def restart_handler(event):
            try:
                await event.edit("🔄 Перезапуск бота...")
                await self.module_manager.load_all_modules()
                await event.edit("✅ Все модули перезагружены!")
            except Exception as e:
                logger.error(f"Ошибка при .start: {e}")
                await event.edit("❌ Ошибка при перезапуске.")
                await event.respond(
                    "📄 Логи доступны по кнопке:",
                    buttons=[Button.inline("📄 Показать лог", b"show_log")]
                )

        @self.client.on(events.NewMessage(pattern=r'\.\s*hello'))
        async def hello_handler(event):
            await event.edit("🤖 Бот активен!")
            
        @self.client.on(events.CallbackQuery(data=b"show_log"))
        async def show_log_handler(event):
            path = Path("logs/bot.log")
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    last_lines = "".join(f.readlines()[-15:])
                await event.respond("📄 Последние строки лога:\n\n" + f"<pre>{last_lines}</pre>", parse_mode="html")
            else:
                await event.respond("❌ Лог-файл не найден.")

    async def start(self):
        await self.client.start()
        print(f"Client is connected: {self.client.is_connected()}")
        await self.setup_handlers()
        await self.module_manager.load_all_modules("modules")
        await self.module_manager.load_all_modules("../out_modules")
        await self.notify_restart()
        print("Клиент запущен") 
        print(f"Загруженные модули: {list(self.module_manager.modules.keys())}")
        await self.client.run_until_disconnected()