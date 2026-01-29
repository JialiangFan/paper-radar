## daily_news_email

Sends daily email containing the latest news articles from NewsAPI.

### Requirements

- Python **3.10+**
- Dependencies: `requests`, `PyYAML`, `python-dotenv`, `newsapi-python`

Install:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### NewsAPI API key

1. Create an account at [NewsAPI.org](https://newsapi.org/).
2. Get your API key from the dashboard.
3. Set environment variable:

```bash
export NEWS_API_KEY="your-api-key-here"
```

### Configuration

Create `config.yaml` (or start from `config.example.yaml`). Required fields:

- `email`: sender/recipient settings (Mailgun-first or SMTP fallback)
- `country`: ISO 3166-1 alpha-2 country code (e.g., "us", "gb")
- `language`: ISO 639-1 language code (e.g., "en")

All secrets can be overridden via environment variables (see below).

Example:

```bash
cp config.example.yaml config.yaml
```

### Environment variable overrides

- NewsAPI:
  - `NEWS_API_KEY` (required)
  - `NEWS_COUNTRY` (default: "us")
  - `NEWS_LANGUAGE` (default: "en")
  - `NEWS_CATEGORY` (optional: business, entertainment, general, health, science, sports, technology)
  - `NEWS_QUERY` (optional: search query)
  - `NEWS_MAX_ARTICLES` (default: 10)
- Email (paper_agent compatible Mailgun-first):
  - `USE_MAILGUN_API=true`
  - `MAILGUN_API_KEY`
  - `MAILGUN_DOMAIN`
  - Optional: `MAILGUN_BASE_URL` (default: `https://api.mailgun.net`)
- Email SMTP fallback (overrides `email.*` in config):
  - `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `EMAIL_FROM`, `EMAIL_TO`
    - `EMAIL_TO` may be a comma-separated list
- Optional:
  - `DNSE_ENV_FILE` (path to .env file)
  - `DNSE_DEBUG=1`

### Run

Dry run (prints email only):

```bash
python -m daily_news_email run --config config.yaml --dry-run
```

Send email:

```bash
python -m daily_news_email run --config config.yaml
```

Debug logs:

```bash
python -m daily_news_email run --config config.yaml --dry-run --debug
```

Test email:

```bash
python -m daily_news_email test-email --config config.yaml
```

### Systemd Timer example

Daily at 12:30 AM Eastern Time:

```ini
[Unit]
Description=Daily News Email Timer (12:30 AM EST/EDT)
Requires=daily-news-email.service

[Timer]
OnCalendar=*-*-* 00:30:00 America/New_York
Persistent=true

[Install]
WantedBy=timers.target
```

### Notes

- Free tier of NewsAPI has rate limits (100 requests/day)
- Articles are filtered to include only those with title and URL
- Email format is plain text for maximum compatibility
