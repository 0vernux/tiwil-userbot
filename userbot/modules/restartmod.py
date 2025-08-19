
import os 
import sys 
from core.loader import Module, tds

@tds 
class RestartMod(Module):
    """Перезапускает бота""" 
    strings = {"name": "RestartMod"}

    async def rescmd(self, message):
        await message.edit("♻️ Перезапускаюсь...")
    
        # Сохраняем chat_id и msg_id
        try:
            with open("restart_info.json", "w") as f:
                import json
                json.dump({
                    "chat_id": message.chat_id,
                    "msg_id": message.id
                }, f)
        except Exception as e:
            await message.respond(f"⚠️ Не удалось сохранить инфо о перезапуске: <code>{e}</code>", parse_mode="html")
    
        # Перезапуск бота через execv (жесткий рестарт)
        os.execv(sys.executable, [sys.executable, "main.py"])