# Daily Coding Challenge Telegram Bot

## Overview

This project implements a Telegram bot that generates daily coding challenges using Google's Gemini AI and delivers them to a specified Telegram chat. The bot supports multiple programming languages, each with its own context and difficulty settings, ensuring a diverse and engaging learning experience.

## Features

*   **AI-Powered Challenge Generation**: Leverages Google Gemini AI to create unique coding challenges, complete with problem statements, setup instructions, pro-tips, lessons, test files, and boilerplate code.
*   **Multi-Language Support**: Configurable to generate challenges in various programming languages (e.g., Java, JavaScript, Python, Go), each with specific idiomatic contexts.
*   **Pydantic Configuration Validation**: Ensures robust and type-safe configuration management using Pydantic v2.
*   **Asynchronous Design**: Built with `asyncio` and `python-telegram-bot` (v20+) for efficient, non-blocking I/O operations.
*   **Telegram Delivery**: Parses and sends the challenge summary (problem, pro-tip, lesson) as a text message, followed by the full Markdown file directly to a Telegram chat or channel.
*   **GitHub Actions Automation**: Scheduled workflows to automatically generate and send challenges daily.

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── daily_challenge.yml  # GitHub Actions workflow for daily runs
├── src/
│   ├── main.py                  # Main application entry point
│   ├── config/
│   │   └── schema.py            # Pydantic schemas for configuration validation
│   ├── services/
│   │   ├── ai_engine.py         # Handles interaction with Google Gemini AI
│   │   └── telegram_service.py  # Handles interaction with Telegram Bot API
│   └── strategies/
│       └── language_strategy.py # Strategy pattern for language-specific prompts
├── config.yaml                  # Main configuration file for languages and settings
└── requirements.txt             # Python dependencies
```

## Setup

### Prerequisites

*   Python 3.11+
*   Git

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/daily-coding-challenge-telegram.git
cd daily-coding-challenge-telegram
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure `config.yaml`

The `config.yaml` file defines the languages and their properties for challenge generation. You can customize this file to add or modify languages, difficulties, test frameworks, and setup commands.

```yaml
languages:
  - name: "Java"
    difficulty: "medium"
    test_framework: "JUnit 5"
    setup_cmd: "mvn test"
  - name: "JavaScript"
    difficulty: "medium"
    test_framework: "Jest"
    setup_cmd: "npm install && npm test"
  - name: "Python"
    difficulty: "easy"
    test_framework: "unittest"
    setup_cmd: "python3 -m unittest"
  - name: "Go"
    difficulty: "easy"
    test_framework: "testing"
    setup_cmd: "go test"
```

### 4. Set Environment Variables / GitHub Secrets

The bot requires the following environment variables to be set. For local testing, you can set them in your shell. For deployment with GitHub Actions, you *must* set them as repository secrets.

*   **`TELEGRAM_TOKEN`**: Your Telegram Bot API token, obtained from [@BotFather](https://t.me/botfather).
*   **`TELEGRAM_CHAT_ID`**: The ID of the Telegram chat or channel where the bot will send the challenges. You can get this by forwarding a message from your channel/group to [@RawDataBot](https://t.me/RawDataBot) or similar bots.
*   **`GEMINI_API_KEY`**: Your API key for Google Gemini, obtained from [Google AI Studio](https://aistudio.google.com/app/apikey).

#### For GitHub Actions:

Go to your repository on GitHub -> `Settings` -> `Secrets and variables` -> `Actions` -> `New repository secret` and add each of the above variables.

## Usage

### Running Locally (for testing)

To test the bot locally, ensure your environment variables are set, then run:

```bash
PYTHONPATH=. python src/main.py
```

This will generate a challenge and send it to your configured Telegram chat.

### Running with GitHub Actions

The `.github/workflows/daily_challenge.yml` workflow is configured to:

*   Run daily at 8:00 AM UTC.
*   Be manually triggerable via `workflow_dispatch`.

To trigger a run manually:
1.  Go to the `Actions` tab in your GitHub repository.
2.  Select the "Daily Coding Challenge Bot" workflow.
3.  Click "Run workflow" on the right side.

## Contributing

Feel free to fork the repository, open issues, or submit pull requests.

## License

This project is open-sourced under the MIT License. See the LICENSE file for details.
