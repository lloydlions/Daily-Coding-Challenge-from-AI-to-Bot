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
Create one concise daily learning challenge.

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

If the topic is code-reading, include a short realistic script to inspect, ask the learner to explain behavior or predict output, then make a small practical change.
Use varied realistic mini-scenarios such as API payloads, logs, CSV rows, config data, carts, tasks, scores, user records, file paths, or validation reports. Do not repeat one fixed sample app or domain.
Avoid trivial tasks like creating variables, adding two numbers, basic loop/if drills, isolated function-definition drills, or syntax examples with no practical data transformation.
Keep it practical and compact. Use no more than 6 assertions.
Do not include Selenium, browser automation, or UI automation.
"""
        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
