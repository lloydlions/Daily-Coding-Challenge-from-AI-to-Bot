import asyncio
import random
import yaml
from dotenv import load_dotenv # Import load_dotenv
from config.schema import BotConfig
from strategies.language_strategy import get_strategy
from services.ai_engine import AIEngine
from services.telegram_service import TelegramService

async def main():
    # Load environment variables from .env file
    load_dotenv() 

    print("Loading configuration...")
    with open("config.yaml", "r") as f:
        config = BotConfig.model_validate(yaml.safe_load(f))
        
    print("Selecting random challenge parameters...")
    selected_lang = random.choice(config.languages)
    strategy = get_strategy(selected_lang.name)
    context = strategy.get_prompt_context()
    
    print(f"Generating {selected_lang.difficulty} challenge for {selected_lang.name}...")
    ai = AIEngine()
    
    # Executing asynchronous generation call
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

if __name__ == "__main__":
    asyncio.run(main())