from core import loader
import platform
import sys
import os

@loader.tds
class EnvInfoMod(loader.Module):
    """Информация об окружении"""

    strings = {"name": "EnvInfo"}

    async def envcmd(self, message):
        """Показывает технические детали окружения"""
        try:
            python_version = sys.version.split()[0]
            system = platform.system()
            release = platform.release()
            modules_dir = "modules"
            core_dir = "core"

            modules_loaded = len(self.bot.module_manager.modules)
            modules_total = len([
                name for name in os.listdir(modules_dir)
                if name.endswith(".py") and not name.startswith("_")
            ])

            log_path = "logs/bot.log"
            log_exists = os.path.exists(log_path)

            await message.edit(
                f"<b>🧬 Окружение:</b>\n\n"
                f"🖥️ Система: <code>{system} {release}</code>\n"
                f"🐍 Python: <code>{python_version}</code>\n"
                f"📦 Модулей: <code>{modules_loaded}</code> загружено из <code>{modules_total}</code>\n"
                f"📁 Логи: {'✅' if log_exists else '❌'} (<code>{log_path}</code>)",
                parse_mode="html"
            )
        except Exception as e:
            await message.edit(f"❌ Ошибка при получении окружения: <code>{e}</code>", parse_mode="html")