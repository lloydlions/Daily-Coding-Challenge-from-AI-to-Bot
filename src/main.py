import asyncio
import os
from datetime import datetime
from zoneinfo import ZoneInfo

import yaml
from dotenv import load_dotenv

from config.schema import BotConfig
from services.ai_engine import AIEngine
from services.telegram_service import TelegramService
from services.topic_selector import TopicSelector
from services.topic_store import TopicStore


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config.yaml")
CATALOG_PATH = os.path.join(PROJECT_ROOT, "data", "topic_catalog.yaml")
HISTORY_PATH = os.path.join(PROJECT_ROOT, "data", "topic_history.json")


def load_yaml(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


async def main():
    load_dotenv(os.path.join(PROJECT_ROOT, ".env"))
    try:
        print("Loading configuration...")
        config = BotConfig.model_validate(load_yaml(CONFIG_PATH))
        catalog = load_yaml(CATALOG_PATH)

        today = datetime.now(ZoneInfo(config.timezone))
        weekday = today.strftime("%A").lower()
        track_key = config.weekly_schedule.get(weekday)

        if not track_key:
            print(f"{weekday.title()} is a rest day. No challenge generated.")
            return

        track = config.get_track(track_key)
        topic_store = TopicStore(HISTORY_PATH)
        history = topic_store.load()
        selected_topic = TopicSelector(catalog).select(track.key, history)

        print(f"Generating {track.difficulty} {track.name} challenge: {selected_topic.topic}")
        ai = AIEngine()
        content = await ai.generate_challenge(
            track=track.name,
            topic=selected_topic.topic,
            lang=track.language,
            difficulty=track.difficulty,
            framework=track.test_framework,
            setup_cmd=track.setup_cmd,
            context=track.context,
        )

        print("Delivering challenge via Telegram...")
        ts = TelegramService()
        await ts.send_bundle(content)

        topic_store.append(
            {
                "date": today.date().isoformat(),
                "track": track.key,
                "track_name": track.name,
                "language": track.language,
                "difficulty": track.difficulty,
                "topic": selected_topic.topic,
            }
        )
        print("Topic history updated.")
        print("Process complete!")
    except Exception as e:
        print(f"Error encountered: {e}")
        try:
            ts = TelegramService()
            await ts.send_error(e)
        except Exception as notify_err:
            print(f"Failed to send error to Telegram: {notify_err}")


if __name__ == "__main__":
    asyncio.run(main())
