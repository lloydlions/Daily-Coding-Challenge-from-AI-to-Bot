import os

from openai import AsyncOpenAI


class AIEngine:
    def __init__(self):
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is missing.")
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.model_name = "qwen/qwen-2.5-7b-instruct"

    async def generate_challenge(
        self,
        track: str,
        topic: str,
        lang: str,
        difficulty: str,
        framework: str,
        setup_cmd: str,
        context: str,
    ) -> str:
        prompt = f"""
Create one concise daily coding challenge.

Track: {track}
Language: {lang}
Difficulty: {difficulty}
Topic: {topic}
Test framework: {framework}
Setup command: {setup_cmd}
Context: {context}

Return Markdown using exactly these headings:
### Daily Coding Challenge: [Creative Title]
**Track:** {track} | **Language:** {lang} | **Difficulty:** {difficulty}
### Problem Statement
### Setup & Dependencies
### Pro-Tip
### Lesson: [Key Concept]
### Test File
### Boilerplate

Keep it practical and compact. Use no more than 8 assertions.
Do not include Selenium, browser automation, or UI automation.
"""
        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
