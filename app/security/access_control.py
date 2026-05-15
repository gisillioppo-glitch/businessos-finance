"""Simple access control helpers for the Streamlit dashboard MVP."""

import hmac

from app.security.config import settings


ALLOWED_ROLES = {
    "admin": [
        "Dashboard",
        "Alerts",
        "Finance",
        "Operations",
        "Governance",
        "Sensitivity",
        "Support",
        "Assistance",
        "Approvals",
        "Daily Close",
        "Scheduled Close",
        "Notifications",
        "Delivery Approval",
        "Secure Email",
        "System Integrity",
        "Release Readiness",
        "Runtime Stability",
        "Surface Audit",
        "Boundary Index",
        "Session Handoff",
        "Demo Readiness",
        "Demo Package",
        "Demo Script",
        "Pilot Plan",
        "Pilot Tracker",
        "Pilot Exit",
        "Pilot Day 1",
        "Pilot Day 2",
        "Pilot Day 3",
        "Pilot Day 4",
        "Pilot Day 5",
        "Pilot Expansion",
        "People",
    ],
    "executive": [
        "Dashboard",
        "Alerts",
        "Finance",
        "Operations",
        "Governance",
        "Sensitivity",
        "Support",
        "Assistance",
        "Approvals",
        "Daily Close",
        "Scheduled Close",
        "Notifications",
        "Delivery Approval",
        "Secure Email",
        "System Integrity",
        "Release Readiness",
        "Runtime Stability",
        "Surface Audit",
        "Boundary Index",
        "Session Handoff",
        "Demo Readiness",
        "Demo Package",
        "Demo Script",
        "Pilot Plan",
        "Pilot Tracker",
        "Pilot Exit",
        "Pilot Day 1",
        "Pilot Day 2",
        "Pilot Day 3",
        "Pilot Day 4",
        "Pilot Day 5",
        "Pilot Expansion",
        "People",
    ],
    "viewer": [
        "Dashboard",
        "Alerts",
        "Finance",
        "Operations",
        "Governance",
        "Sensitivity",
        "Support",
        "Assistance",
        "Approvals",
        "Daily Close",
        "Scheduled Close",
        "Notifications",
        "Delivery Approval",
        "Secure Email",
        "System Integrity",
        "Release Readiness",
        "Runtime Stability",
        "Surface Audit",
        "Boundary Index",
        "Session Handoff",
        "Demo Readiness",
        "Demo Package",
        "Demo Script",
        "Pilot Plan",
        "Pilot Tracker",
        "Pilot Exit",
        "Pilot Day 1",
        "Pilot Day 2",
        "Pilot Day 3",
        "Pilot Day 4",
        "Pilot Day 5",
        "Pilot Expansion",
        "People",
    ],
}


def validate_credentials(username, password):
    username_matches = hmac.compare_digest(username, settings.admin_username)
    password_matches = hmac.compare_digest(password, settings.admin_password)
    return username_matches and password_matches


def get_default_role(username):
    if username == settings.admin_username:
        return "admin"

    return "viewer"


def get_allowed_pages(role):
    return ALLOWED_ROLES.get(role, ALLOWED_ROLES["viewer"])











