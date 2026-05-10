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

    @property
    def using_default_password(self):
        return self.admin_password == DEFAULT_LOCAL_PASSWORD


settings = SecuritySettings()
