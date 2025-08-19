from core import loader
import inspect
import types

@loader.tds
class HelpMod(loader.Module):
    """Показывает справку по модулям и командам"""

    strings = {"name": "Help"}

    async def helpcmd(self, message):
        """Показывает это сообщение"""
        modules = self.bot.module_manager.modules

        if not modules:
            return await message.edit("❌ Модули не загружены.")

        help_text = "<b>📖 Список команд и модулей:</b>\n\n"

        for name, mod in modules.items():
            title = getattr(mod, "strings", {}).get("name", name)

            if isinstance(mod, loader.Module):
                desc = inspect.getdoc(mod) or "Без описания"
                commands = [m[:-3] for m in dir(mod) if m.endswith("cmd")]
            elif isinstance(mod, types.ModuleType):
                desc = inspect.getdoc(mod) or "Без описания"
                commands = []
            else:
                desc = "Без описания"
                commands = []

            help_text += f"📦 <b>{title}</b>: {desc}\n"
            if commands:
                help_text += " • " + "\n • ".join([f"<code>.{cmd}</code>" for cmd in commands]) + "\n"
            help_text += "\n"

        await message.edit(help_text, parse_mode="html")

    async def modinfocmd(self, message):
        """Показывает описание конкретного модуля"""
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            return await message.edit("❗ Укажи имя модуля.")

        mod_name = args[1].strip()

        # Получаем module_manager
        manager = getattr(self.bot, "module_manager", None)
        if not manager:
            return await message.edit("❌ Менеджер модулей не найден.")

        doc = manager.module_docs.get(mod_name)
        loaded = mod_name in manager.modules

        if doc is None:
            return await message.edit(f"❌ Модуль `{mod_name}` не найден.")

        await message.edit(
            f"📦 <b>{mod_name}</b>\n"
            f"{'✅ Загружен' if loaded else '❌ Не загружен'}\n"
            f"📝 Описание: {doc}",
            parse_mode="html"
        )