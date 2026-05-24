from abc import ABC, abstractmethod

class LanguageStrategy(ABC):
    @abstractmethod
    def get_prompt_context(self) -> str:
        pass

class JavaStrategy(LanguageStrategy):
    def get_prompt_context(self) -> str:
        return "Use idiomatic Java 17+. Focus on clean object-oriented design and standard collections."

class JavaScriptStrategy(LanguageStrategy):
    def get_prompt_context(self) -> str:
        return "Use modern ES6+ JavaScript. Focus on functional array methods and clean syntax."

class PythonStrategy(LanguageStrategy):
    def get_prompt_context(self) -> str:
        return "Use idiomatic Python (PEP 8). Focus on list comprehensions and standard library modules."

class GoStrategy(LanguageStrategy):
    def get_prompt_context(self) -> str:
        return "Use idiomatic Go. Focus on simplicity, error handling, and standard library modules."

def get_strategy(language_name: str) -> LanguageStrategy:
    strategies = {
        "Java": JavaStrategy(),
        "JavaScript": JavaScriptStrategy(),
        "Python": PythonStrategy(),
        "Go": GoStrategy()
    }
    return strategies.get(language_name, PythonStrategy())