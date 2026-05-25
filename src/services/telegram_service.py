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
            
        # Extract sections using regex
        title_match = re.search(r"### 🧩 (.*?)\n", content)
        title = title_match.group(1).strip() if title_match else "Daily Coding Challenge"
        
        problem_match = re.search(r"### 📝 Problem Statement\n(.*?)\n### ⚙️", content, re.DOTALL)
        problem = problem_match.group(1).strip() if problem_match else "See document for problem statement."
        
        protip_match = re.search(r"### 💡 Pro-Tip\n(.*?)\n### 🎓", content, re.DOTALL)
        protip = protip_match.group(1).strip() if protip_match else ""
        
        lesson_match = re.search(r"### 🎓 Lesson:(.*?)\n(.*?)\n### 🧪", content, re.DOTALL)
        if lesson_match:
            lesson_title = lesson_match.group(1).strip()
            lesson = lesson_match.group(2).strip()
        else:
            lesson_title = "Key Concept"
            lesson = ""

        message_text = f"🚀 {title}\n\n📝 Problem Statement\n{problem}\n\n💡 Pro-Tip\n{protip}\n\n🎓 Lesson: {lesson_title}\n{lesson}"
        if len(message_text) > 4000:
            message_text = message_text[:4000] + "...\n\n(See attached file for the full challenge)"
        
        async with self.bot:
            # Send text message first
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message_text
            )
            # Then send the full markdown file
            with open(filename, 'rb') as f:
                await self.bot.send_document(
                    chat_id=self.chat_id, 
                    document=f, 
                    caption="💻 Here is the full code setup and boilerplate!"
                )