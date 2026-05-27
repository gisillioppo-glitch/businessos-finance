from types import MappingProxyType


BUSINESSOS_EVIDENCE_REPORTS = (
    MappingProxyType(
        {
            "label": "Command Center",
            "file_prefix": "command_center",
            "purpose": "Unified executive system summary.",
        }
    ),
    MappingProxyType(
        {
            "label": "Executive Alerts",
            "file_prefix": "executive_alerts",
            "purpose": "Cross-module executive alert queue.",
        }
    ),
    MappingProxyType(
        {
            "label": "Approval Decisions",
            "file_prefix": "approval_decisions",
            "purpose": "Approval outcomes, decisions, and justifications.",
        }
    ),
    MappingProxyType(
        {
            "label": "Governance Brief",
            "file_prefix": "governance_brief",
            "purpose": "Governance posture and audit trail health.",
        }
    ),
    MappingProxyType(
        {
            "label": "Support Brief",
            "file_prefix": "support_brief",
            "purpose": "Support incident status and next move.",
        }
    ),
    MappingProxyType(
        {
            "label": "Daily Finance Brief",
            "file_prefix": "daily_brief",
            "purpose": "Finance health, risks, and recommended actions.",
        }
    ),
)


BUSINESSOS_DEPARTMENT_REPORTS = MappingProxyType(
    {
        "Executive": (
            "Command Center",
            "Executive Alerts",
            "Approval Decisions",
            "Governance Brief",
            "Support Brief",
            "Daily Finance Brief",
        ),
        "Finance": ("Daily Finance Brief", "Command Center", "Executive Alerts"),
        "Operations": ("Command Center", "Executive Alerts", "Approval Decisions"),
        "Governance": ("Governance Brief", "Approval Decisions", "Executive Alerts"),
        "Support": ("Support Brief", "Executive Alerts", "Command Center"),
    }
)


BUSINESSOS_EVIDENCE_CONFIG = MappingProxyType(
    {
        "branch_id": "businessos",
        "statuses": frozenset({"available", "missing"}),
        "evidence_reports": BUSINESSOS_EVIDENCE_REPORTS,
        "department_reports": BUSINESSOS_DEPARTMENT_REPORTS,
        "default_distribution_reports": (
            "Command Center",
            "Executive Alerts",
        ),
        "distribution_delivery_mode": "email_ready_queue",
        "distribution_subject_prefix": "BusinessOS Daily Close",
    }
)


def get_evidence_config():
    return BUSINESSOS_EVIDENCE_CONFIG


def get_evidence_reports():
    return get_evidence_config()["evidence_reports"]


def get_evidence_statuses():
    return get_evidence_config()["statuses"]


def get_department_reports():
    return get_evidence_config()["department_reports"]


def get_default_distribution_reports():
    return get_evidence_config()["default_distribution_reports"]


def get_distribution_delivery_mode():
    return get_evidence_config()["distribution_delivery_mode"]


def get_distribution_subject_prefix():
    return get_evidence_config()["distribution_subject_prefix"]
