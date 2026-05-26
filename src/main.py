import asyncio
import random
import os
import yaml
from dotenv import load_dotenv
from config.schema import BotConfig
from strategies.language_strategy import get_strategy
from services.ai_engine import AIEngine
from services.telegram_service import TelegramService

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

async def main():
    load_dotenv(os.path.join(PROJECT_ROOT, ".env"))
    try:
        print("Loading configuration...")
        with open(os.path.join(PROJECT_ROOT, "config.yaml"), "r") as f:
            config = BotConfig.model_validate(yaml.safe_load(f))
            
        print("Selecting random challenge parameters...")
        selected_lang = random.choice(config.languages)
        strategy = get_strategy(selected_lang.name)
        context = strategy.get_prompt_context()
        
        print(f"Generating {selected_lang.difficulty} challenge for {selected_lang.name}...")
        ai = AIEngine()
        
        content = await ai.generate_challenge(
            lang=selected_lang.name,
            difficulty=selected_lang.difficulty,
            framework=selected_lang.test_framework,
            context=context
        )
        
        print("Delivering challenge via Telegram...")
        ts = TelegramService()
        await ts.send_bundle(content)
        print("Process complete! 🏁")
    except Exception as e:
        print(f"Error encountered: {e}")
        try:
            ts = TelegramService()
            await ts.send_error(e)
        except Exception as notify_err:
            print(f"Failed to send error to Telegram: {notify_err}")

if __name__ == "__main__":
    asyncio.run(main())