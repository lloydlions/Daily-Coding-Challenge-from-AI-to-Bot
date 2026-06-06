import json
from pathlib import Path
from typing import Any


class TopicStore:
    def __init__(self, path: str | Path, max_entries: int = 30):
        self.path = Path(path)
        self.max_entries = max_entries

    def load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []

        with self.path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError(f"Topic history must be a JSON array: {self.path}")

        return data[-self.max_entries :]

    def append(self, entry: dict[str, Any]) -> None:
        history = self.load()
        history.append(entry)
        history = history[-self.max_entries :]

        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
            f.write("\n")
