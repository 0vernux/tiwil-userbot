
def dummy_decorator(func=None, *args, **kwargs):
    if func is None:
        return lambda f: f
    return func

owner = dummy_decorator
sudo = dummy_decorator
assistant = dummy_decorator
only_me = dummy_decorator
private = dummy_decorator
public_cmd = dummy_decorator
admin = dummy_decorator


class Module:
    """Базовый FTG-модуль"""
    def __init__(self):
        self.config = {}
        self.client = None
        self.bot = None

def tds(cls):
    """Просто возвращает класс — декоратор-заглушка"""
    return cls