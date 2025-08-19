from core import loader 
import requests 
import re 
import os

@loader.tds 
class ModuleManage(loader.Module): 
    """Управление модулями: загрузка, выгрузка, перезагрузка, удаление"""

    strings = {"name": "ModuleManage"}
    
    async def unloadcmd(self, message):
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            return await message.edit("❗ Укажи имя модуля для выгрузки.")
        mod_name = args[1].strip()
        success = await self.bot.module_manager.unload_module(mod_name)
        if success:
            await message.edit(f"✅ Модуль `{mod_name}` выгружен.")
        else:
            await message.edit(f"❌ Модуль `{mod_name}` не найден или не загружен.")
    
    async def reloadcmd(self, message):
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            return await message.edit("❗ Укажи имя модуля для перезагрузки.")
        mod_name = args[1].strip()
        success = await self.bot.module_manager.reload_module(mod_name)
        if success:
            await message.edit(f"🔁 Модуль `{mod_name}` перезагружен.")
        else:
            await message.edit(f"❌ Не удалось перезагрузить `{mod_name}`.")
    
    async def loadcmd(self, message):
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            return await message.edit("❗ Укажи имя файла модуля (без `.py`).")
        mod_name = args[1].strip()
        path = self.bot.module_manager.find_module_path(mod_name)
        if not path:
            return await message.edit("❌ Модуль не найден.")
        success = await self.bot.module_manager.load_module(path)
        await message.edit(
            f"✅ Модуль `{mod_name}` загружен." if success else f"❌ Не удалось загрузить `{mod_name}`."
        )
    
    async def loadmodcmd(self, message):
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            return await message.edit("❗ Укажи ссылку на модуль.")
    
        url = args[1].strip()
    
        # Если это GitHub blob-ссылка — преобразуем в raw
        if "github.com" in url and "/blob/" in url:
            url = re.sub(r"github\\.com/([^/]+/[^/]+)/blob/(.+)", r"raw.githubusercontent.com/\1/\2", url)
            url = "https://" + url
    
        module_name = url.split("/")[-1].replace(".py", "")
    
        try:
            r = requests.get(url)
            code = r.content.decode("utf-8", errors="ignore")
    
            # Убираем мусор и нормализуем код
            code = code.replace('\ufeff', '').replace('\u00A0', ' ').replace('\t', ' ')
            code = re.sub(r'from\\s+\\.\\.\\s+import', 'from core import', code)
            code = re.sub(r'from\\s+\\.\\.([a-zA-Z0-9_]+)\\s+import', r'from core.\1 import', code)
            
            os.makedirs("../out_modules", exist_ok=True)
            path = f"../out_modules/{module_name}.py"
            with open(path, "w", encoding="utf-8") as f:
                f.write(code)
    
            success = await self.bot.module_manager.load_module(path)
            await message.edit(
                f"✅ Модуль `{module_name}` загружен!" if success else f"❌ Не удалось загрузить `{module_name}`."
            )
    
        except Exception as e:
            await message.edit(f"❌ Ошибка загрузки: `{e}`")
    
    async def delmodcmd(self, message):
        """Удаляет модуль (.py) после выгрузки"""
    
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            return await message.edit("❗️ Укажи имя модуля для удаления.")
    
        mod_name = args[1].strip()
        path = self.bot.module_manager.find_module_path(mod_name)
    
        if not path:
            return await message.edit(f"❌ Файл модуля `{mod_name}.py` не найден.")
    
        # Попробуем выгрузить модуль, если он загружен
        unloaded = await self.bot.module_manager.unload_module(mod_name)
        if unloaded:
            await message.edit(f"🔁 Модуль `{mod_name}` выгружен, удаляю файл...")
        else:
            await message.edit(f"⚠️ Модуль `{mod_name}` не был загружен, но файл всё равно будет удалён...")
    
        try:
            os.remove(path)
            await message.edit(f"🗑 Модуль `{mod_name}` успешно удалён.")
        except Exception as e:
            await message.edit(f"❌ Ошибка при удалении файла: `{e}`")
    
    async def modscmd(self, message):
        """Показывает статус всех модулей (встроенных и внешних)"""
        from pathlib import Path

        loaded = list(self.bot.module_manager.modules.keys())
        text = "📦 <b>Статус модулей:</b>\n\n"

        # Встроенные модули
        internal = list(Path("modules").glob("*.py"))
        text += "<u>🧩 Встроенные модули:</u>\n"
        count_int_loaded = 0

        for file in sorted(internal):
            name = file.stem
            if name in loaded:
                text += f"✅ <code>{file.name}</code>\n"
                count_int_loaded += 1
            else:
                text += f"❌ <code>{file.name}</code>\n"

        # Внешние модули
        external = list(Path("../out_modules").glob("*.py"))
        text += "\n<u>🧪 Внешние модули:</u>\n"
        count_ext_loaded = 0

        for file in sorted(external):
            name = file.stem
            if name in loaded:
                text += f"✅ <code>{file.name}</code>\n"
                count_ext_loaded += 1
            else:
                text += f"❌ <code>{file.name}</code>\n"

        total_int = len(internal)
        total_ext = len(external)

        text += (
            f"\n<b>Итого:</b>\n"
            f"🧩 Встроенных: <b>{total_int}</b> | ✅ Загружено: <b>{count_int_loaded}</b>\n"
            f"🧪 Внешних: <b>{total_ext}</b> | ✅ Загружено: <b>{count_ext_loaded}</b>"
        )

        await message.edit(text, parse_mode="html")