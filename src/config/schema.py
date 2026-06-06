from typing import Optional

from pydantic import BaseModel


class TrackConfig(BaseModel):
    key: str
    name: str
    language: str
    difficulty: str
    test_framework: str
    setup_cmd: str
    context: str


class BotConfig(BaseModel):
    timezone: str = "Asia/Manila"
    weekly_schedule: dict[str, Optional[str]]
    tracks: list[TrackConfig]

    def get_track(self, key: str) -> TrackConfig:
        for track in self.tracks:
            if track.key == key:
                return track
        raise ValueError(f"Track '{key}' is missing from config.yaml.")
