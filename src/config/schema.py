from pydantic import BaseModel
from typing import List

class LanguageConfig(BaseModel):
    name: str
    difficulty: str
    test_framework: str
    setup_cmd: str

class BotConfig(BaseModel):
    languages: List[LanguageConfig]