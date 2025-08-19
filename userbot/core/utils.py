def get_args(message):
    """Разбивает текст на аргументы"""
    return message.raw_text.split(maxsplit=1)[1:] if len(message.raw_text.split()) > 1 else []

async def answer(message, text, **kwargs):
    """Быстро ответить в чат"""
    return await message.respond(text, **kwargs)

def parse_arguments(args: str) -> list[str]:
    """Разбить строку аргументов по пробелам"""
    return args.strip().split()

def split_by_limit(text, limit=4096):
    """Разделить длинный текст на куски по лимиту Telegram"""
    return [text[i:i+limit] for i in range(0, len(text), limit)]