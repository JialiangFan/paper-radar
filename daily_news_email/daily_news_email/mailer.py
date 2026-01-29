from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage

import requests


def send_email_via_smtp(
    *,
    smtp_host: str,
    smtp_port: int,
    smtp_user: str | None,
    smtp_password: str | None,
    from_addr: str,
    to_addrs: list[str],
    subject: str,
    body: str,
    use_ssl: bool | None = None,
    use_starttls: bool | None = None,
    debug: bool = False,
) -> None:
    if use_ssl is None and use_starttls is None:
        # Common defaults
        if int(smtp_port) == 465:
            use_ssl = True
            use_starttls = False
        else:
            use_ssl = False
            use_starttls = True

    msg = EmailMessage()
    msg["From"] = from_addr
    msg["To"] = ", ".join(to_addrs)
    msg["Subject"] = subject
    msg.set_content(body)

    if use_ssl:
        server: smtplib.SMTP = smtplib.SMTP_SSL(smtp_host, int(smtp_port), timeout=30)
    else:
        server = smtplib.SMTP(smtp_host, int(smtp_port), timeout=30)

    try:
        if debug:
            server.set_debuglevel(1)
        server.ehlo()
        if use_starttls:
            server.starttls()
            server.ehlo()
        if smtp_user and smtp_password:
            server.login(smtp_user, smtp_password)
        server.send_message(msg)
    finally:
        try:
            server.quit()
        except Exception:
            pass


def send_email_via_mailgun(
    *,
    mailgun_api_key: str,
    mailgun_domain: str,
    from_addr: str,
    to_addrs: list[str],
    subject: str,
    body: str,
    timeout_sec: int = 30,
    base_url: str | None = None,
) -> None:
    """
    Send a plain-text email via Mailgun HTTP API.

    Mirrors paper_agent style:
    - env vars: MAILGUN_API_KEY, MAILGUN_DOMAIN, USE_MAILGUN_API
    """
    if not mailgun_api_key:
        raise ValueError("MAILGUN_API_KEY is required for Mailgun sending")
    if not mailgun_domain:
        raise ValueError("MAILGUN_DOMAIN is required for Mailgun sending")

    if base_url is None:
        base_url = os.getenv("MAILGUN_BASE_URL", "https://api.mailgun.net").rstrip("/")

    url = f"{base_url}/v3/{mailgun_domain}/messages"
    data = {
        "from": from_addr,
        "to": ", ".join(to_addrs),  # Mailgun expects a string
        "subject": subject,
        "text": body,
    }
    resp = requests.post(url, auth=("api", mailgun_api_key), data=data, timeout=timeout_sec)
    if resp.status_code == 200:
        return
    raise RuntimeError(f"Mailgun API error {resp.status_code}: {resp.text[:500]}")


def send_email(
    *,
    # If USE_MAILGUN_API=true and creds exist, Mailgun is attempted first (fallback to SMTP).
    smtp_host: str | None = None,
    smtp_port: int | None = None,
    smtp_user: str | None = None,
    smtp_password: str | None = None,
    from_addr: str,
    to_addrs: list[str],
    subject: str,
    body: str,
    use_ssl: bool | None = None,
    use_starttls: bool | None = None,
    debug: bool = False,
    mailgun_api_key: str | None = None,
    mailgun_domain: str | None = None,
) -> None:
    use_mailgun_api = os.getenv("USE_MAILGUN_API", "false").strip().lower() == "true"

    if use_mailgun_api:
        mg_key = mailgun_api_key or os.getenv("MAILGUN_API_KEY", "")
        mg_domain = mailgun_domain or os.getenv("MAILGUN_DOMAIN", "")
        if mg_key and mg_domain:
            try:
                return send_email_via_mailgun(
                    mailgun_api_key=mg_key,
                    mailgun_domain=mg_domain,
                    from_addr=from_addr,
                    to_addrs=to_addrs,
                    subject=subject,
                    body=body,
                )
            except Exception as e:
                # paper_agent behavior: fallback to SMTP
                if debug:
                    print(f"[mailer] Mailgun failed, falling back to SMTP: {e}")

    if not smtp_host or smtp_port is None:
        raise ValueError("SMTP config missing and Mailgun not enabled/working")

    return send_email_via_smtp(
        smtp_host=smtp_host,
        smtp_port=int(smtp_port),
        smtp_user=smtp_user,
        smtp_password=smtp_password,
        from_addr=from_addr,
        to_addrs=to_addrs,
        subject=subject,
        body=body,
        use_ssl=use_ssl,
        use_starttls=use_starttls,
        debug=debug,
    )
