"""Security settings for the local BusinessOS MVP."""

import os

DEFAULT_LOCAL_USERNAME = "admin"
DEFAULT_LOCAL_PASSWORD = "businessos-local"


class SecuritySettings:
    def __init__(self):
        self.app_env = os.getenv("BUSINESSOS_APP_ENV", "local")
        self.admin_username = os.getenv(
            "BUSINESSOS_ADMIN_USERNAME",
            DEFAULT_LOCAL_USERNAME,
        )
        self.admin_password = os.getenv(
            "BUSINESSOS_ADMIN_PASSWORD",
            DEFAULT_LOCAL_PASSWORD,
        )
        self.email_delivery_enabled = _env_flag("BUSINESSOS_EMAIL_DELIVERY_ENABLED", False)
        self.email_delivery_dry_run = _env_flag("BUSINESSOS_EMAIL_DELIVERY_DRY_RUN", True)
        self.smtp_host = os.getenv("BUSINESSOS_SMTP_HOST")
        self.smtp_port = _env_int("BUSINESSOS_SMTP_PORT", 587)
        self.smtp_username = os.getenv("BUSINESSOS_SMTP_USERNAME")
        self.smtp_password = os.getenv("BUSINESSOS_SMTP_PASSWORD")
        self.smtp_from_email = os.getenv("BUSINESSOS_SMTP_FROM_EMAIL")
        self.smtp_use_tls = _env_flag("BUSINESSOS_SMTP_USE_TLS", True)
        self.smtp_timeout_seconds = _env_int("BUSINESSOS_SMTP_TIMEOUT_SECONDS", 10)

    @property
    def using_default_password(self):
        return self.admin_password == DEFAULT_LOCAL_PASSWORD

    @property
    def email_delivery_configured(self):
        return all(
            [
                self.smtp_host,
                self.smtp_port,
                self.smtp_username,
                self.smtp_password,
                self.smtp_from_email,
            ]
        )


def _env_flag(name, default=False):
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name, default):
    value = os.getenv(name)

    if not value:
        return default

    return int(value)


settings = SecuritySettings()
