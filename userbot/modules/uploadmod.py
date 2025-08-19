from core.loader import Module, tds
import os
from pathlib import Path

@tds
class UploadModModule(Module):
    """Загрузка .py модуля через реплай"""
    strings = {"name": "UploadMod"}

    def init(self):
        super().init()
        self.name = self.strings["name"]

    async def uploadmodcmd(self, message):
        reply = await message.get_reply_message()
        if not reply or not reply.file or not reply.file.name.endswith(".py"):
            return await message.edit("❌ Реплай должен быть на .py файл", parse_mode="html")

        filename = reply.file.name
        if filename == ".py":
            return await message.edit("❌ Имя файла не может быть .py — переименуй файл", parse_mode="html")

        # Сохраняем в папку, находящуюся на уровень выше папки с ботом (в tiwil/out_modules)
        base_dir = Path(__file__).resolve().parent.parent.parent  # <- tiwil/
        out_path = base_dir / "out_modules"
        out_path.mkdir(exist_ok=True)

        path = out_path / filename

        await message.edit("📦 Загружаю модуль...", parse_mode="html")

        # Скачиваем файл
        await self.client.download_media(reply.media, file=str(path))

        # Пробуем перезагрузить
        try:
            self.bot.module_manager.load_module(str(path))  # исправлено
            await message.edit(f"✅ Модуль <b>{filename}</b> успешно загружен!", parse_mode="html")
        except Exception as e:
            await message.edit(
                f"⚠️ Модуль <b>{filename}</b> загружен, но не удалось перезагрузить.\n<code>{e}</code>",
                parse_mode="html"
            )