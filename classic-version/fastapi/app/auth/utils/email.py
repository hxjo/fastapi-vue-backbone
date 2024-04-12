from pathlib import Path
from typing import Any, Dict, Optional

import emails
from emails.template import JinjaTemplate

from app.core.config import settings


def send_email(
    email_to: str,
    subject: str = "",
    html_template: str = "",
    environment: Optional[Dict[str, Any]] = None,
) -> None:
    environment = environment or {}
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=subject,
        html=JinjaTemplate(html_template),
        mail_from=(settings.PROJECT_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    message.send(to=email_to, render=environment, smtp=smtp_options)


def send_reset_password_email(email_to: str, username: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {username}"
    with open(
        Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html", encoding="utf-8"
    ) as f:
        template_str = f.read()
    frontend_url = settings.FRONTEND_HOST
    link = f"{frontend_url}/auth/reset-password?token={token}"
    send_email(
        email_to=email_to,
        subject=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )
