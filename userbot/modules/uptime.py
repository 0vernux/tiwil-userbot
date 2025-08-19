import time
from core import loader

@loader.tds
class UptimeMod(loader.Module):
    """Показывает, сколько времени бот работает без перезапуска"""

    strings = {"name": "Uptime"}

    def __init__(self):
        self._start_time = time.time()

    async def uptimecmd(self, message):
        """Показать аптайм (.uptime)"""
        now = time.time()
        delta = int(now - self._start_time)

        hours, rem = divmod(delta, 3600)
        minutes, seconds = divmod(rem, 60)

        formatted = f"{hours}ч {minutes}м {seconds}с"
        await message.edit(f"🕒 Аптайм: <code>{formatted}</code>", parse_mode="html")