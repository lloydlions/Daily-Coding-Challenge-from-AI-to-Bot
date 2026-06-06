import os
import re

from telegram import Bot


class TelegramService:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if not self.token or not self.chat_id:
            raise ValueError("Telegram credentials missing in environment.")
        self.bot = Bot(token=self.token)

    async def send_bundle(self, content: str, filename: str = "daily_challenge.md"):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

        # Extract sections using stable ASCII headings from the AI prompt.
        title_match = re.search(r"### Daily Coding Challenge: (.*?)\n", content)
        title = title_match.group(1).strip() if title_match else "Daily Coding Challenge"

        problem_match = re.search(r"### Problem Statement\n(.*?)\n### Setup & Dependencies", content, re.DOTALL)
        problem = problem_match.group(1).strip() if problem_match else "See document for problem statement."

        protip_match = re.search(r"### Pro-Tip\n(.*?)\n### Lesson:", content, re.DOTALL)
        protip = protip_match.group(1).strip() if protip_match else ""

        lesson_match = re.search(r"### Lesson:(.*?)\n(.*?)\n### Test File", content, re.DOTALL)
        if lesson_match:
            lesson_title = lesson_match.group(1).strip()
            lesson = lesson_match.group(2).strip()
        else:
            lesson_title = "Key Concept"
            lesson = ""

        message_text = f"{title}\n\nProblem Statement\n{problem}\n\nPro-Tip\n{protip}\n\nLesson: {lesson_title}\n{lesson}"
        if len(message_text) > 4000:
            message_text = message_text[:4000] + "...\n\n(See attached file for the full challenge)"

        async with self.bot:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message_text,
            )
            with open(filename, "rb") as f:
                await self.bot.send_document(
                    chat_id=self.chat_id,
                    document=f,
                    caption="Full code setup and boilerplate",
                )

    async def send_error(self, error: Exception):
        message = f"Error encountered: {error}"
        async with self.bot:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
            )
