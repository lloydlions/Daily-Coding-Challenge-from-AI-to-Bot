import random
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SelectedTopic:
    track_key: str
    topic: str


class TopicSelector:
    def __init__(self, catalog: dict[str, Any]):
        self.catalog = catalog

    def select(self, track_key: str, history: list[dict[str, Any]]) -> SelectedTopic:
        topics = self._topics_for(track_key)
        recent_topics = {
            entry.get("topic")
            for entry in history
            if entry.get("track") == track_key
        }
        available_topics = [topic for topic in topics if topic not in recent_topics]

        if not available_topics:
            available_topics = topics

        return SelectedTopic(
            track_key=track_key,
            topic=random.choice(available_topics),
        )

    def _topics_for(self, track_key: str) -> list[str]:
        tracks = self.catalog.get("tracks", {})
        track = tracks.get(track_key)
        if not track:
            raise ValueError(f"Track '{track_key}' is missing from topic catalog.")

        topics = track.get("topics", [])
        if not topics:
            raise ValueError(f"Track '{track_key}' has no topics in topic catalog.")

        return topics
