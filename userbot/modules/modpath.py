from core import loader

@loader.tds
class ModPath(loader.Module):
    """Показывает путь до .py-файла модуля"""
    
    strings = {"name": "ModPath"}

    async def modpathcmd(self, message):
        """<имя> — путь к модулю"""
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            return await message.edit("❗ Укажи имя модуля, пример: `.modpath loader`")

        mod_name = args[1].strip()

        path = self.bot.module_manager.module_paths.get(mod_name)
        if path:
            await message.edit(f"📁 Путь к модулю `{mod_name}`:\n<code>{path}</code>", parse_mode="html")
        else:
            await message.edit(f"❌ Модуль `{mod_name}` не найден или не загружен.")