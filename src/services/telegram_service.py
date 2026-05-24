from telegram import Bot
import os

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
        
        with open(filename, 'rb') as f:
            await self.bot.send_document(
                chat_id=self.chat_id, 
                document=f, 
                caption="🚀 Here is your daily coding challenge, pro-tip, and lesson!"
            )