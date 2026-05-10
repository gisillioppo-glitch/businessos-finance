import sqlite3
import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.security.access_control import (  # noqa: E402
    get_allowed_pages,
    get_default_role,
    validate_credentials,
)
from app.security.config import settings  # noqa: E402

DB_PATH = ROOT_DIR / "finance.db"


def get_count(query, params=None):
    if params is None:
        params = ()

    conn = sqlite3.connect(DB_PATH)

    try:
        return conn.execute(query, params).fetchone()[0]
    finally:
        conn.close()


def load_dashboard_data():
    transactions_count = get_count("SELECT COUNT(*) FROM transactions")

    active_finance_actions = get_count(
        """
        SELECT COUNT(*)
        FROM recommended_actions
        WHERE status IN ('open', 'in_progress')
        """
    )

    active_operations_tasks = get_count(
        """
        SELECT COUNT(*)
        FROM operations_tasks
        WHERE status IN ('open', 'in_progress', 'blocked')
        """
    )

    overdue_operations_tasks = get_count(
        """
        SELECT COUNT(*)
        FROM operations_tasks
        WHERE status IN ('open', 'in_progress', 'blocked')
          AND deadline_date IS NOT NULL
          AND deadline_date < date('now')
        """
    )

    active_support_incidents = get_count(
        """
        SELECT COUNT(*)
        FROM support_incidents
        WHERE status IN ('open', 'investigating', 'waiting')
        """
    )

    governance_findings = get_count(
        """
        SELECT COUNT(*)
        FROM audit_logs
        WHERE event_type = 'governance_finding_detected'
        """
    )

    error_events = get_count(
        """
        SELECT COUNT(*)
        FROM audit_logs
        WHERE severity IN ('error', 'critical')
        """
    )

    if error_events > 0 or active_support_incidents > 0 or overdue_operations_tasks > 0:
        overall_health = "Needs Attention"
        highest_risk = "High"
        next_move = "Resolve active support incidents and overdue operations tasks."
    elif active_operations_tasks > 0 or active_finance_actions > 0:
        overall_health = "Watch"
        highest_risk = "Medium"
        next_move = "Review active actions and operations tasks."
    else:
        overall_health = "Healthy"
        highest_risk = "None"
        next_move = "Maintain current operating cadence."

    return {
        "transactions_count": transactions_count,
        "active_finance_actions": active_finance_actions,
        "active_operations_tasks": active_operations_tasks,
        "overdue_operations_tasks": overdue_operations_tasks,
        "active_support_incidents": active_support_incidents,
        "governance_findings": governance_findings,
        "error_events": error_events,
        "overall_health": overall_health,
        "highest_risk": highest_risk,
        "next_move": next_move,
    }


def render_login():
    st.title("BusinessOS Command Center")
    st.caption("Private executive dashboard. Sign in to continue.")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign in")

    if submitted:
        if validate_credentials(username, password):
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.session_state["role"] = get_default_role(username)
            st.rerun()

        st.error("Invalid username or password.")

    if settings.using_default_password:
        st.warning(
            "Local MVP credentials are active. Change BUSINESSOS_ADMIN_PASSWORD before deploying."
        )

    st.stop()


def render_sidebar():
    role = st.session_state.get("role", "viewer")
    username = st.session_state.get("username", "user")
    allowed_pages = get_allowed_pages(role)

    st.sidebar.title("BusinessOS")
    st.sidebar.caption(f"Signed in as {username} ({role})")

    page = st.sidebar.radio("Navigation", allowed_pages)

    if st.sidebar.button("Refresh"):
        st.rerun()

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    return page


def main():
    st.set_page_config(
        page_title="BusinessOS Command Center",
        page_icon="B",
        layout="wide",
    )

    if not st.session_state.get("authenticated"):
        render_login()

    page = render_sidebar()
    data = load_dashboard_data()

    if page == "Dashboard":
        st.title("BusinessOS Command Center")
        st.caption("Unified executive view across Finance, Operations, Governance, and Support.")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Overall Health", data["overall_health"])
        col2.metric("Highest Risk", data["highest_risk"])
        col3.metric("Support Incidents", data["active_support_incidents"])
        col4.metric("Overdue Ops Tasks", data["overdue_operations_tasks"])

        st.subheader("Executive Brief")
        st.write(f"**Next best executive move:** {data['next_move']}")

        st.subheader("Module Snapshot")

        c1, c2 = st.columns(2)

        with c1:
            st.write("### Finance")
            st.metric("Transactions", data["transactions_count"])
            st.metric("Active finance actions", data["active_finance_actions"])

            st.write("### Operations")
            st.metric("Active operations tasks", data["active_operations_tasks"])
            st.metric("Overdue operations tasks", data["overdue_operations_tasks"])

        with c2:
            st.write("### Governance")
            st.metric("Governance findings", data["governance_findings"])
            st.metric("Error/Critical events", data["error_events"])

            st.write("### Support")
            st.metric("Active support incidents", data["active_support_incidents"])

    elif page == "Finance":
        st.title("Finance")
        st.metric("Transactions", data["transactions_count"])
        st.metric("Active finance actions", data["active_finance_actions"])

    elif page == "Operations":
        st.title("Operations")
        st.metric("Active operations tasks", data["active_operations_tasks"])
        st.metric("Overdue operations tasks", data["overdue_operations_tasks"])

    elif page == "Governance":
        st.title("Governance")
        st.metric("Governance findings", data["governance_findings"])
        st.metric("Error/Critical events", data["error_events"])

    elif page == "Support":
        st.title("Support")
        st.metric("Active support incidents", data["active_support_incidents"])


if __name__ == "__main__":
    main()
