from __future__ import annotations

import argparse
import os
from pathlib import Path

from .config import apply_env_overrides, load_config
from .email_builder import build_email
from .mailer import send_email
from .news_client import NewsClient


def _maybe_load_dotenv(debug: bool, config_path: str | None = None) -> None:
    try:
        from dotenv import load_dotenv  # type: ignore

        # 1) Current working directory
        load_dotenv(override=False)

        # 2) Optional explicit env file
        explicit = os.getenv("DNSE_ENV_FILE")
        if explicit:
            load_dotenv(dotenv_path=explicit, override=False)

        # 3) Nearby to config: config dir and one parent up
        if config_path:
            cfg_p = Path(config_path).expanduser().resolve()
            for candidate in [cfg_p.parent / ".env", cfg_p.parent.parent / ".env"]:
                if candidate.exists():
                    load_dotenv(dotenv_path=candidate, override=False)

        if debug:
            print("[debug] Loaded .env files (if present)")
    except Exception:
        return


def _require(cfg: dict, path: str):
    cur = cfg
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            raise ValueError(f"Missing required config field: {path}")
        cur = cur[part]
    return cur


def run_once(config_path: str, dry_run: bool, debug: bool) -> int:
    """Fetch news and send email"""
    _maybe_load_dotenv(debug, config_path=config_path)

    cfg_obj = load_config(config_path)
    cfg = apply_env_overrides(cfg_obj.raw)

    # Get NewsAPI key
    news_api_key = cfg.get("news_api_key") or os.getenv("NEWS_API_KEY")
    if not news_api_key:
        raise ValueError("NEWS_API_KEY is required (set in config or environment)")

    # Initialize news client
    client = NewsClient(api_key=news_api_key, debug=debug)

    # Get configuration
    country = cfg.get("country", "us")
    language = cfg.get("language", "en")
    category = cfg.get("category")
    query = cfg.get("query")
    max_articles = int(cfg.get("max_articles", 10))
    use_everything = cfg.get("use_everything", False)

    if debug:
        print(f"[debug] Config: country={country}, language={language}, category={category}, query={query}")

    # Fetch news
    if use_everything or query:
        # Use get_everything for custom queries
        articles = client.get_everything(
            q=query,
            language=language,
            page_size=max_articles * 2,  # Get more to filter
        )
    else:
        # Use top headlines
        articles = client.get_top_headlines(
            country=country,
            category=category,
            q=query,
            page_size=max_articles * 2,
        )

    if not articles:
        if debug:
            print("[debug] No articles found")
        articles = []

    # Filter out articles without title or URL
    articles = [a for a in articles if a.get("title") and a.get("url")]

    # Limit to max_articles
    articles = articles[:max_articles]

    # Build email
    email_title = cfg.get("email_title", "Daily News Digest")
    email = build_email(articles=articles, title=email_title, max_articles=max_articles)

    if dry_run:
        print(f"Subject: {email.subject}\n")
        print(email.body)
    else:
        from_addr = _require(cfg, "email.from")
        to_addrs = _require(cfg, "email.to")
        if isinstance(to_addrs, str):
            to_addrs = [to_addrs]

        # Get SMTP config
        smtp_host = cfg.get("email", {}).get("smtp_host")
        smtp_port = cfg.get("email", {}).get("smtp_port")
        smtp_user = cfg.get("email", {}).get("smtp_user")
        smtp_password = cfg.get("email", {}).get("smtp_password")

        send_email(
            smtp_host=str(smtp_host) if smtp_host else None,
            smtp_port=int(smtp_port) if smtp_port is not None else None,
            smtp_user=str(smtp_user) if smtp_user else None,
            smtp_password=str(smtp_password) if smtp_password else None,
            from_addr=str(from_addr),
            to_addrs=[str(t) for t in to_addrs],
            subject=email.subject,
            body=email.body,
            debug=debug,
        )

        if debug:
            print(f"[debug] Email sent successfully to {len(to_addrs)} recipient(s)")

    return 0


def send_test_email(config_path: str, debug: bool) -> int:
    """Send a test email"""
    _maybe_load_dotenv(debug, config_path=config_path)

    cfg_obj = load_config(config_path)
    cfg = apply_env_overrides(cfg_obj.raw)

    from_addr = _require(cfg, "email.from")
    to_addrs = _require(cfg, "email.to")
    if isinstance(to_addrs, str):
        to_addrs = [to_addrs]

    smtp_host = cfg.get("email", {}).get("smtp_host")
    smtp_port = cfg.get("email", {}).get("smtp_port")
    smtp_user = cfg.get("email", {}).get("smtp_user")
    smtp_password = cfg.get("email", {}).get("smtp_password")

    subject = "Daily News Email Test"
    body = (
        "This is a test email from daily_news_email.\n\n"
        "If you received this, email configuration works.\n"
    )

    send_email(
        smtp_host=str(smtp_host) if smtp_host else None,
        smtp_port=int(smtp_port) if smtp_port is not None else None,
        smtp_user=str(smtp_user) if smtp_user else None,
        smtp_password=str(smtp_password) if smtp_password else None,
        from_addr=str(from_addr),
        to_addrs=[str(t) for t in to_addrs],
        subject=subject,
        body=body,
        debug=debug,
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="daily_news_email")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run_p = sub.add_parser("run", help="Fetch news and send email")
    run_p.add_argument("--config", required=True, help="Path to config.yaml or config.json")
    run_p.add_argument("--dry-run", action="store_true", help="Print email to stdout, do not send")
    run_p.add_argument("--debug", action="store_true", help="Verbose logs (no secrets)")

    test_p = sub.add_parser("test-email", help="Send a simple test email")
    test_p.add_argument("--config", required=True, help="Path to config.yaml or config.json")
    test_p.add_argument("--debug", action="store_true", help="Verbose logs (no secrets)")

    args = parser.parse_args(argv)

    if args.cmd == "run":
        return run_once(args.config, dry_run=bool(args.dry_run), debug=bool(args.debug))
    if args.cmd == "test-email":
        return send_test_email(args.config, debug=bool(args.debug))

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
