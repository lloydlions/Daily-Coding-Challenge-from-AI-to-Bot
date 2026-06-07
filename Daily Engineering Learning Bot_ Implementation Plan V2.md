# Daily Engineering Learning Bot: Current Implementation Plan

## Goal

Generate one compact daily learning challenge through Telegram while keeping token usage low and avoiding recent topic repeats.

The bot should stay standalone and schedule-driven. Changing priorities should only require editing `config.yaml` and `data/topic_catalog.yaml`, not rewriting application code.

The current configured track is Python with foundational difficulty. It follows the early Python course phases as a concept guide while skipping already-known control-flow basics. It focuses on:

- reading realistic small Python scripts across varied domains
- practicing lists, dictionaries, sets, and tuples
- translating JavaScript array-helper or Java stream habits into Python idioms
- using comprehensions, `sorted`, `any`, `all`, `zip`, `enumerate`, `Counter`, and `defaultdict`
- transforming JSON-like payloads, rows, logs, config data, and records into stable outputs
- making practical script changes rather than toy exercises

Sunday is a rest day.

## Schedule

The schedule is configured in `config.yaml`.

| Day | Track |
| --- | --- |
| Monday | Python |
| Tuesday | Python |
| Wednesday | Python |
| Thursday | Python |
| Friday | Python |
| Saturday | Python |
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
