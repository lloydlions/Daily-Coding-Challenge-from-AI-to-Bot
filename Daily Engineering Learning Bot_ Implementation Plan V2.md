# Daily Engineering Learning Bot: Current Implementation Plan

## Goal

Generate one compact daily programming challenge through Telegram while keeping token usage low and avoiding recent topic repeats.

The learning path is intentionally broad but focused:

- Java Core
- Quarkus
- SQL
- Python Data Basics
- AI/API Mini Tasks
- Review / Mixed Practice

Sunday is a rest day.

## Schedule

The schedule is configured in `config.yaml`.

| Day | Track |
| --- | --- |
| Monday | Java Core |
| Tuesday | Quarkus |
| Wednesday | SQL |
| Thursday | Python Data Basics |
| Friday | AI/API Mini Task |
| Saturday | Review / Mixed Practice |
| Sunday | Rest |

## Token Strategy

The bot does not ask the model to choose a topic. The topic is selected locally from `data/topic_catalog.yaml`, then sent to the model in a compact prompt.

This reduces token usage because the prompt only includes:

- track
- language
- difficulty
- topic
- test framework
- setup command
- short context

## Repeat Prevention

`data/topic_history.json` stores the newest 30 generated topic entries.

The topic selector avoids topics already present in recent history for the same track. If every catalog topic for a track has already appeared in recent history, it allows reuse so the bot can keep running.

History is updated only after Telegram delivery succeeds.

## Persistence

GitHub Actions commits `data/topic_history.json` back to the repository after each successful run.

This is simpler and more reliable than artifacts or cache for this project because the next scheduled run can read the history directly from the checked-out repository.

## GitHub Actions

The workflow runs Monday-Saturday at 8:00 AM Asia/Manila:

```yaml
cron: "0 0 * * 1-6"
```

The workflow uses:

```yaml
permissions:
  contents: write
```

Required secrets:

- `TELEGRAM_TOKEN`
- `TELEGRAM_CHAT_ID`
- `OPENROUTER_API_KEY`

## Main Flow

1. Load `.env`, `config.yaml`, and `data/topic_catalog.yaml`.
2. Determine the current weekday in the configured timezone.
3. Exit if the day is configured as rest.
4. Load the rolling topic history.
5. Select a topic for the day's track.
6. Generate a concise Markdown challenge with OpenRouter.
7. Send the Telegram summary and full Markdown document.
8. Append the topic to `data/topic_history.json`.
9. Let GitHub Actions commit the updated history file.

## Current Runtime Files

- `src/main.py`
- `src/config/schema.py`
- `src/services/ai_engine.py`
- `src/services/telegram_service.py`
- `src/services/topic_selector.py`
- `src/services/topic_store.py`
- `config.yaml`
- `data/topic_catalog.yaml`
- `data/topic_history.json`
- `.github/workflows/daily_challenge.yml`
