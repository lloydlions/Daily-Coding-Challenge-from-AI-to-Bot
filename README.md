# Daily Coding Challenge Telegram Bot

This project generates a compact daily coding challenge with an AI model and sends it to Telegram.

The bot is schedule-driven and configurable. Tracks, topics, difficulty, framework, timezone, and rest days are controlled through configuration files instead of hardcoded application logic.

## How It Works

1. Reads the current day in the configured timezone.
2. Selects the track assigned to that day in `config.yaml`.
3. Selects a recent-unused topic from `data/topic_catalog.yaml`.
4. Generates a concise Markdown challenge through OpenRouter.
5. Sends a Telegram summary and the full Markdown file.
6. Saves the used topic in `data/topic_history.json`.

## Repeat Prevention

Used topics are saved in `data/topic_history.json`, which is kept to the newest 30 entries. The topic selector avoids recent repeats for the same track.

In GitHub Actions, the workflow commits `data/topic_history.json` back to the repository after a successful run so the next scheduled run can read the latest history.

## Features

- Configurable weekday schedule
- Configurable tracks and topic catalog
- Sunday/rest-day support
- Rolling 30-entry topic history
- Compact prompts to reduce token usage
- Telegram summary plus full Markdown document
- GitHub Actions automation

## Setup

### Requirements

- Python 3.11+
- Telegram bot token
- OpenRouter API key

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file for local runs:

```env
TELEGRAM_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID="YOUR_TELEGRAM_CHAT_ID"
OPENROUTER_API_KEY="YOUR_OPENROUTER_API_KEY"
```

Run locally:

```bash
PYTHONPATH=. python src/main.py
```

## Configuration

- `config.yaml`: timezone, weekly schedule, tracks, difficulty, framework, setup command, and prompt context
- `data/topic_catalog.yaml`: topic pools per track
- `data/topic_history.json`: rolling history of generated topics

## GitHub Actions

Add these repository secrets:

- `TELEGRAM_TOKEN`
- `TELEGRAM_CHAT_ID`
- `OPENROUTER_API_KEY`

The workflow currently runs Monday-Saturday at 8:00 AM Asia/Manila:

```yaml
cron: "0 0 * * 1-6"
```

The workflow needs `contents: write` permission so it can commit `data/topic_history.json` after a successful challenge.
