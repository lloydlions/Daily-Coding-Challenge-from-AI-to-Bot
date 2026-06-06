# Daily Coding Challenge Telegram Bot

This project generates a compact daily learning challenge with an AI model and sends it to Telegram.

The bot now follows a weekly learning schedule instead of choosing a random language. It is designed for steady programming growth with Java, Quarkus, SQL, beginner Python data work, and small AI/API tasks. Sunday is a rest day.

## Current Schedule

| Day | Track |
| --- | --- |
| Monday | Java Core |
| Tuesday | Quarkus |
| Wednesday | SQL |
| Thursday | Python Data Basics |
| Friday | AI/API Mini Task |
| Saturday | Review / Mixed Practice |
| Sunday | Rest |

The schedule is configured in `config.yaml`.

## Repeat Prevention

Topics are selected locally from `data/topic_catalog.yaml` before the AI call. This keeps prompts small and avoids spending tokens on topic selection.

Used topics are saved in `data/topic_history.json`, which is kept to the newest 30 entries. The GitHub Actions workflow commits that file back to the repository after a successful run so the next scheduled run can avoid recent repeats.

## Features

- OpenRouter-powered challenge generation through the OpenAI-compatible SDK
- Telegram delivery of a readable summary plus the full Markdown file
- Weekday-based learning tracks
- Sunday rest day
- Rolling 30-entry topic history
- Compact prompts to reduce token usage
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

## GitHub Actions

Add these repository secrets:

- `TELEGRAM_TOKEN`
- `TELEGRAM_CHAT_ID`
- `OPENROUTER_API_KEY`

The workflow runs Monday-Saturday at 8:00 AM Asia/Manila:

```yaml
cron: "0 0 * * 1-6"
```

The workflow needs `contents: write` permission so it can commit `data/topic_history.json` after a successful challenge.

## Customizing Topics

Edit `data/topic_catalog.yaml` to add or remove topics. Keep topics short because they are passed directly into the AI prompt.

Edit `config.yaml` to adjust tracks, difficulty, framework, setup command, context, timezone, or weekly schedule.
