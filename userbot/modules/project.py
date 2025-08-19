from core import loader
from pathlib import Path

@loader.tds
class ProjectStructureMod(loader.Module):
    """Показывает структуру проекта."""

    strings = {"name": "Project"}

    def get_structure(self, path: Path, prefix="") -> str:
        entries = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        tree = ""
        for i, entry in enumerate(entries):
            connector = "└── " if i == len(entries) - 1 else "├── "
            tree += f"{prefix}{connector}{entry.name}\n"
            if entry.is_dir() and entry.name not in ("__pycache__", ".git"):
                extension = "    " if i == len(entries) - 1 else "│   "
                tree += self.get_structure(entry, prefix + extension)
        return tree

    async def projectcmd(self, message):
        """Показать структуру проекта"""
        base_path = Path(".")
        tree = self.get_structure(base_path)
        await message.edit(f"<b>📁 Структура проекта:</b>\n<pre>{tree}</pre>", parse_mode="html")