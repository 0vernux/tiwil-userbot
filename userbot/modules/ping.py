"""
показывает задержку бота
• .ping
"""

import time
from telethon import events

def setup(bot):
    @bot.client.on(events.NewMessage(pattern=r'\.\s*ping'))
    async def ping_handler(event):
        start = time.perf_counter()
        msg = await event.edit("🏓")
        end = time.perf_counter()

        latency_ms = round((end - start) * 1000)
        await msg.edit(f"🚀 {latency_ms}ms")