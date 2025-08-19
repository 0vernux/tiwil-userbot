import importlib.util
import glob
import sys
import ast
import os
from pathlib import Path
from typing import Dict, Any
from telethon import events
from core.logger_mod import logger

class ModuleManager:
    def __init__(self, bot):
        self.bot = bot
        self.modules: Dict[str, Any] = {}
        self.module_docs: Dict[str, str] = {}        # Описание
        self.module_handlers: Dict[str, list] = {}   # Хендлеры
        self.module_paths: Dict[str, str] = {}       # Путь к .py

    def find_module_path(self, mod_name: str) -> str | None:
        for base in ["modules", "../out_modules"]:
            path = os.path.join(base, f"{mod_name}.py")
            if os.path.isfile(path):
                return path
        return None

    async def load_module(self, module_path: str) -> bool:
        def make_handler(m):
            async def handler(event):
                await m(event)
            return handler

        try:
            module_name = Path(module_path).stem

            if module_name in self.modules:
                logger.warning(f"Модуль {module_name} уже загружен, пропуск.")
                return False

            with open(module_path, "r", encoding="utf-8") as f:
                content = f.read()

            if "from .. import loader" in content:
                content = content.replace("from .. import loader", "from core import loader")
                with open(module_path, "w", encoding="utf-8") as f:
                    f.write(content)

            parsed = ast.parse(content)
            module_docstring = ast.get_docstring(parsed) or "Без описания"
            self.module_docs[module_name] = module_docstring

            if module_name.startswith('_'):
                return False

            spec = importlib.util.spec_from_file_location(f"modules.{module_name}", module_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[f"modules.{module_name}"] = module
            spec.loader.exec_module(module)

            self.module_docs[module_name] = module.__doc__.strip() if module.__doc__ else "Без описания"

            loaded = False
            handlers = []

            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type):
                    bases = getattr(attr, '__bases__', [])
                    if any(base.__name__ == 'Module' for base in bases):
                        mod_instance = attr()
                        mod_instance.client = self.bot.client
                        mod_instance.bot = self.bot

                        for name in dir(mod_instance):
                            if name.endswith("cmd"):
                                method = getattr(mod_instance, name)
                                if callable(method):
                                    cmd_name = name[:-3]
                                    pattern = rf"^\.{cmd_name}(?:\s+|$)(.*)"
                                    handler = make_handler(method)
                                    self.bot.client.add_event_handler(
                                        handler,
                                        events.NewMessage(pattern=pattern)
                                    )
                                    handlers.append((handler, pattern))

                        self.modules[module_name] = mod_instance
                        self.module_handlers[module_name] = handlers
                        self.module_paths[module_name] = module_path  # ⬅️ добавлено
                        loaded = True
                        break

            if not loaded and hasattr(module, 'setup'):
                setup_result = module.setup(self.bot)
                if hasattr(setup_result, '__await__'):
                    await setup_result
                self.modules[module_name] = module
                self.module_handlers[module_name] = []
                self.module_paths[module_name] = module_path  # ⬅️ добавлено
                loaded = True

            return loaded

        except Exception as e:
            logger.error(f"Ошибка загрузки модуля {module_path}: {str(e)}")
            return False

    async def unload_module(self, module_name: str) -> bool:
        if module_name in self.modules:
            module = self.modules[module_name]

            for handler, pattern in self.module_handlers.get(module_name, []):
                try:
                    self.bot.client.remove_event_handler(handler, events.NewMessage(pattern=pattern))
                except Exception as e:
                    logger.warning(f"Не удалось удалить хендлер {pattern}: {e}")

            if hasattr(module, 'teardown'):
                await module.teardown(self.bot)

            del self.modules[module_name]
            del sys.modules[f"modules.{module_name}"]
            self.module_docs.pop(module_name, None)
            self.module_handlers.pop(module_name, None)
            self.module_paths.pop(module_name, None)  # ⬅️ удаляем путь

            return True
        return False

    async def reload_module(self, module_name: str) -> bool:
        if module_name in self.modules:
            await self.unload_module(module_name)

        internal_path = f"modules/{module_name}.py"
        external_path = f"../out_modules/{module_name}.py"

        if Path(internal_path).exists():
            return await self.load_module(internal_path)
        elif Path(external_path).exists():
            return await self.load_module(external_path)
        return False

    async def load_all_modules(self, internal_dir: str = "modules", external_dir: str = "../out_modules") -> int:
        loaded = 0

        for module_path in glob.glob(f"{internal_dir}/*.py"):
            if await self.load_module(module_path):
                loaded += 1

        for module_path in glob.glob(f"{external_dir}/*.py"):
            if await self.load_module(module_path):
                loaded += 1

        return loaded