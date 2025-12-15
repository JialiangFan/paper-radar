## daily_tv_speaking_email

Sends one daily email containing:
- a short TV-show dialogue snippet (30–60 seconds) extracted from an **English SRT** subtitle file
- a **10-minute speaking practice routine**
- 5 vocabulary items (simple heuristics; no LLM calls)

The subtitle source is the **official OpenSubtitles.com REST API** (Stoplight documentation).

### Requirements

- Python **3.10+**
- Dependencies (minimal): `requests`, `PyYAML`, `python-dotenv` (optional but included)

Install:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### OpenSubtitles API key

1. Create an account at OpenSubtitles.com.
2. Create an API key in your OpenSubtitles API settings.
3. Set environment variables:

```bash
export OS_API_KEY="..."
# Login is recommended/required for downloading on many setups
export OS_USERNAME="..."
export OS_PASSWORD="..."
```

### Configuration

Create `config.yaml` (or start from `config.example.yaml`). Required fields:

- `shows`: list of `{title, season, episode}`
- `email`: sender/recipient settings (Mailgun-first or SMTP fallback)

All secrets can be overridden via environment variables (see below).

Example:

```bash
cp config.example.yaml config.yaml
```

### Environment variable overrides

- OpenSubtitles:
  - `OS_API_KEY`
  - `OS_USERNAME`
  - `OS_PASSWORD`
- Email (paper_agent compatible Mailgun-first):
  - `USE_MAILGUN_API=true`
  - `MAILGUN_API_KEY`
  - `MAILGUN_DOMAIN`
  - Optional: `MAILGUN_BASE_URL` (default: `https://api.mailgun.net`)
- Email SMTP fallback (overrides `email.*` in config):
  - `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `EMAIL_FROM`, `EMAIL_TO`
    - `EMAIL_TO` may be a comma-separated list
- Optional:
  - `DTVSE_STATE_PATH` (default: alongside config file as `state.json`)
  - `DTVSE_SHOW_SELECTION` (`round_robin` default, or `random`)
  - `DTVSE_DEBUG=1`

### Run

Dry run (prints email only):

```bash
python -m daily_tv_speaking_email run --config config.yaml --dry-run
```

Send email:

```bash
python -m daily_tv_speaking_email run --config config.yaml
```

Debug logs (no secrets):

```bash
python -m daily_tv_speaking_email run --config config.yaml --dry-run --debug
```

### Cron example

Daily at 07:30 in the machine’s local timezone (recommended: set `timezone` in `config.yaml`):

```cron
30 7 * * * /path/to/python -m daily_tv_speaking_email run --config /path/to/config.yaml >> /path/to/daily_tv_speaking_email.log 2>&1
```

### Notes

- Snippet deduplication: hashes are stored in `state.json` and a snippet is never re-sent within the last **30 days**.
- Rate-limits: on HTTP **429**, the client applies exponential backoff and retries.
