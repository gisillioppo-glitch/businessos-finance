import sqlite3
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.governance.sensitivity_rules import get_governance_sensitivity_findings  # noqa: E402
from app.security.access_control import (  # noqa: E402
    get_allowed_pages,
    get_default_role,
    validate_credentials,
)
from app.security.config import settings  # noqa: E402

DB_PATH = ROOT_DIR / "finance.db"


CUSTOM_CSS = """
<style>
:root {
    --bos-bg: #070708;
    --bos-panel: #121214;
    --bos-panel-soft: #17171a;
    --bos-border: rgba(255, 255, 255, 0.08);
    --bos-red: #e31b23;
    --bos-red-soft: rgba(227, 27, 35, 0.16);
    --bos-gold: #f4b740;
    --bos-green: #35c46f;
    --bos-text: #f6f4ef;
    --bos-muted: #9d9da5;
}

.stApp {
    background: radial-gradient(circle at top left, rgba(227, 27, 35, 0.10), transparent 30%), var(--bos-bg);
    color: var(--bos-text);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1f0608 0%, #0b0b0d 38%, #080808 100%);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}

section[data-testid="stSidebar"] * {
    color: var(--bos-text);
}

div[data-testid="stSidebarUserContent"] {
    padding-top: 1.4rem;
}

.main .block-container {
    padding-top: 2.1rem;
    max-width: 1280px;
}

h1, h2, h3 {
    letter-spacing: 0;
}

[data-testid="stMetric"] {
    background: transparent;
}

.bos-topbar {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
    margin-bottom: 1.35rem;
}

.bos-title {
    font-size: 2.15rem;
    line-height: 1.08;
    font-weight: 800;
    margin: 0;
}

.bos-subtitle {
    color: var(--bos-muted);
    font-size: 0.98rem;
    margin-top: 0.45rem;
}

.bos-chip {
    border: 1px solid rgba(227, 27, 35, 0.35);
    background: rgba(227, 27, 35, 0.10);
    color: #ffd7d9;
    border-radius: 999px;
    padding: 0.45rem 0.7rem;
    font-size: 0.82rem;
    white-space: nowrap;
}

.bos-card {
    background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.015)), var(--bos-panel);
    border: 1px solid var(--bos-border);
    border-radius: 8px;
    padding: 1.1rem 1.15rem;
    min-height: 138px;
    box-shadow: 0 14px 38px rgba(0, 0, 0, 0.22);
}

.bos-card-title {
    color: #dedce0;
    font-size: 0.95rem;
    font-weight: 650;
    margin-bottom: 0.65rem;
}

.bos-card-value {
    color: var(--bos-text);
    font-size: 2.05rem;
    line-height: 1.05;
    font-weight: 800;
}

.bos-card-value.red {
    color: #ff383f;
}

.bos-card-value.green {
    color: var(--bos-green);
}

.bos-card-value.gold {
    color: var(--bos-gold);
}

.bos-card-caption {
    color: var(--bos-muted);
    font-size: 0.84rem;
    margin-top: 0.55rem;
}

.bos-panel {
    background: var(--bos-panel);
    border: 1px solid var(--bos-border);
    border-radius: 8px;
    padding: 1.2rem 1.35rem;
    min-height: 100%;
    box-shadow: 0 14px 38px rgba(0, 0, 0, 0.20);
}

.bos-section-title {
    font-size: 1.05rem;
    font-weight: 750;
    margin-bottom: 0.85rem;
}

.bos-brief-item {
    display: grid;
    grid-template-columns: 0.75rem 1fr;
    gap: 0.65rem;
    align-items: start;
    margin: 0.82rem 0;
}

.bos-dot {
    width: 0.52rem;
    height: 0.52rem;
    border-radius: 999px;
    background: var(--bos-red);
    margin-top: 0.42rem;
    box-shadow: 0 0 18px rgba(227, 27, 35, 0.6);
}

.bos-item-main {
    color: var(--bos-text);
    font-weight: 650;
    font-size: 0.96rem;
}

.bos-item-sub {
    color: var(--bos-muted);
    font-size: 0.84rem;
    margin-top: 0.1rem;
}

.bos-row {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 0.8rem;
    align-items: center;
    padding: 0.72rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.bos-row:last-child {
    border-bottom: 0;
}

.bos-badge {
    border-radius: 999px;
    padding: 0.25rem 0.58rem;
    font-size: 0.76rem;
    border: 1px solid rgba(255, 255, 255, 0.12);
    color: var(--bos-text);
    white-space: nowrap;
}

.bos-badge.high {
    color: #ff6066;
    border-color: rgba(227, 27, 35, 0.45);
    background: rgba(227, 27, 35, 0.10);
}

.bos-badge.medium {
    color: #ffc066;
    border-color: rgba(244, 183, 64, 0.42);
    background: rgba(244, 183, 64, 0.08);
}

.bos-badge.low, .bos-badge.none, .bos-badge.healthy {
    color: #72e39b;
    border-color: rgba(53, 196, 111, 0.38);
    background: rgba(53, 196, 111, 0.08);
}

.bos-alert-dot {
    display: inline-block;
    width: 0.5rem;
    height: 0.5rem;
    border-radius: 999px;
    margin-right: 0.55rem;
    background: var(--bos-red);
}

.bos-login-card {
    max-width: 460px;
    margin: 7vh auto 0 auto;
    background: var(--bos-panel);
    border: 1px solid var(--bos-border);
    border-radius: 8px;
    padding: 1.4rem;
}

@media (max-width: 900px) {
    .bos-topbar {
        display: block;
    }

    .bos-chip {
        display: inline-block;
        margin-top: 0.8rem;
    }
}
</style>
"""


def get_scalar(query, params=None):
    if params is None:
        params = ()

    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute(query, params).fetchone()[0]


def get_rows(query, params=None):
    if params is None:
        params = ()

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        return [dict(row) for row in conn.execute(query, params).fetchall()]


def load_cash_flow_series():
    with sqlite3.connect(DB_PATH) as conn:
        frame = pd.read_sql_query(
            """
            SELECT
                date,
                SUM(CASE WHEN type = 'income' THEN amount ELSE -amount END) AS net_cash_flow
            FROM transactions
            GROUP BY date
            ORDER BY date
            """,
            conn,
        )

    if frame.empty:
        return pd.DataFrame({"date": [], "net_cash_flow": []})

    frame["date"] = pd.to_datetime(frame["date"])
    return frame


def load_dashboard_data():
    transactions_count = get_scalar("SELECT COUNT(*) FROM transactions")
    total_income = get_scalar("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = 'income'")
    total_expenses = get_scalar("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = 'expense'")
    net_cash_flow = total_income - total_expenses

    active_finance_actions = get_scalar(
        """
        SELECT COUNT(*)
        FROM recommended_actions
        WHERE status IN ('open', 'in_progress')
        """
    )

    high_finance_actions = get_scalar(
        """
        SELECT COUNT(*)
        FROM recommended_actions
        WHERE status IN ('open', 'in_progress')
          AND priority = 'high'
        """
    )

    active_operations_tasks = get_scalar(
        """
        SELECT COUNT(*)
        FROM operations_tasks
        WHERE status IN ('open', 'in_progress', 'blocked')
        """
    )

    overdue_operations_tasks = get_scalar(
        """
        SELECT COUNT(*)
        FROM operations_tasks
        WHERE status IN ('open', 'in_progress', 'blocked')
          AND deadline_date IS NOT NULL
          AND deadline_date < date('now')
        """
    )

    active_support_incidents = get_scalar(
        """
        SELECT COUNT(*)
        FROM support_incidents
        WHERE status IN ('open', 'investigating', 'waiting')
        """
    )

    critical_support_incidents = get_scalar(
        """
        SELECT COUNT(*)
        FROM support_incidents
        WHERE status IN ('open', 'investigating', 'waiting')
          AND severity IN ('critical', 'high')
        """
    )

    active_assistance_requests = get_scalar(
        """
        SELECT COUNT(*)
        FROM assistance_requests
        WHERE status IN ('open', 'triaged', 'waiting_approval', 'in_progress')
        """
    )

    high_assistance_requests = get_scalar(
        """
        SELECT COUNT(*)
        FROM assistance_requests
        WHERE status IN ('open', 'triaged', 'waiting_approval', 'in_progress')
          AND severity IN ('critical', 'high')
        """
    )

    waiting_approval_requests = get_scalar(
        """
        SELECT COUNT(*)
        FROM assistance_requests
        WHERE status = 'waiting_approval'
        """
    )

    total_people = get_scalar("SELECT COUNT(*) FROM business_users")

    active_people = get_scalar(
        """
        SELECT COUNT(*)
        FROM business_users
        WHERE status = 'active'
        """
    )

    admin_people = get_scalar(
        """
        SELECT COUNT(*)
        FROM business_users
        WHERE access_level = 'admin'
        """
    )

    manager_people = get_scalar(
        """
        SELECT COUNT(*)
        FROM business_users
        WHERE access_level = 'manager'
        """
    )

    governance_findings = get_scalar(
        """
        SELECT COUNT(*)
        FROM audit_logs
        WHERE event_type = 'governance_finding_detected'
        """
    )

    error_events = get_scalar(
        """
        SELECT COUNT(*)
        FROM audit_logs
        WHERE severity IN ('error', 'critical')
        """
    )

    if error_events > 0 or overdue_operations_tasks > 0 or high_assistance_requests > 0:
        overall_health = "Needs Attention"
        highest_risk = "High"
        next_move = "Resolve overdue operations work and triage high-severity assistance requests."
        health_class = "red"
    elif active_support_incidents > 0 or active_operations_tasks > 0 or active_finance_actions > 0 or active_assistance_requests > 0:
        overall_health = "Watch"
        highest_risk = "Medium"
        next_move = "Review active actions, incidents, and operations tasks before expanding workload."
        health_class = "gold"
    else:
        overall_health = "Healthy"
        highest_risk = "None"
        next_move = "Maintain current operating cadence."
        health_class = "green"

    recent_incidents = get_rows(
        """
        SELECT title, severity, status, owner_role
        FROM support_incidents
        ORDER BY created_at DESC
        LIMIT 3
        """
    )

    active_tasks = get_rows(
        """
        SELECT title, priority, status, owner_role
        FROM operations_tasks
        WHERE status IN ('open', 'in_progress', 'blocked')
        ORDER BY
            CASE priority
                WHEN 'critical' THEN 1
                WHEN 'high' THEN 2
                WHEN 'medium' THEN 3
                ELSE 4
            END,
            created_at DESC
        LIMIT 4
        """
    )

    recommended_actions = get_rows(
        """
        SELECT recommended_action, priority, status, owner_role
        FROM recommended_actions
        WHERE status IN ('open', 'in_progress')
        ORDER BY
            CASE priority
                WHEN 'high' THEN 1
                WHEN 'medium' THEN 2
                ELSE 3
            END,
            created_at DESC
        LIMIT 3
        """
    )

    assistance_requests = get_rows(
        """
        SELECT title, request_type, severity, status, owner_role
        FROM assistance_requests
        WHERE status IN ('open', 'triaged', 'waiting_approval', 'in_progress')
        ORDER BY
            CASE severity
                WHEN 'critical' THEN 1
                WHEN 'high' THEN 2
                WHEN 'medium' THEN 3
                WHEN 'low' THEN 4
                ELSE 5
            END,
            created_at DESC
        LIMIT 5
        """
    )

    people_users = get_rows(
        """
        SELECT full_name, email, role, department, status, access_level
        FROM business_users
        ORDER BY
            CASE access_level
                WHEN 'admin' THEN 1
                WHEN 'executive' THEN 2
                WHEN 'manager' THEN 3
                WHEN 'operator' THEN 4
                ELSE 5
            END,
            department,
            full_name
        LIMIT 8
        """
    )

    with sqlite3.connect(DB_PATH) as conn:
        sensitivity_findings = get_governance_sensitivity_findings(conn)

    high_sensitivity_findings = sum(1 for finding in sensitivity_findings if finding["severity"] == "high")
    medium_sensitivity_findings = sum(1 for finding in sensitivity_findings if finding["severity"] == "medium")

    if high_sensitivity_findings > 0:
        highest_sensitivity_risk = "High"
        sensitivity_next_move = "Review high-sensitivity findings and confirm approvals before execution."
    elif medium_sensitivity_findings > 0:
        highest_sensitivity_risk = "Medium"
        sensitivity_next_move = "Review medium-sensitivity findings and confirm ownership."
    else:
        highest_sensitivity_risk = "Low"
        sensitivity_next_move = "Maintain current governance sensitivity controls."

    return {
        "transactions_count": transactions_count,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_cash_flow": net_cash_flow,
        "active_finance_actions": active_finance_actions,
        "high_finance_actions": high_finance_actions,
        "active_operations_tasks": active_operations_tasks,
        "overdue_operations_tasks": overdue_operations_tasks,
        "active_support_incidents": active_support_incidents,
        "critical_support_incidents": critical_support_incidents,
        "active_assistance_requests": active_assistance_requests,
        "high_assistance_requests": high_assistance_requests,
        "waiting_approval_requests": waiting_approval_requests,
        "total_people": total_people,
        "active_people": active_people,
        "admin_people": admin_people,
        "manager_people": manager_people,
        "governance_findings": governance_findings,
        "error_events": error_events,
        "overall_health": overall_health,
        "highest_risk": highest_risk,
        "next_move": next_move,
        "health_class": health_class,
        "recent_incidents": recent_incidents,
        "active_tasks": active_tasks,
        "recommended_actions": recommended_actions,
        "assistance_requests": assistance_requests,
        "people_users": people_users,
        "sensitivity_findings": sensitivity_findings,
        "sensitive_findings": len(sensitivity_findings),
        "high_sensitivity_findings": high_sensitivity_findings,
        "medium_sensitivity_findings": medium_sensitivity_findings,
        "highest_sensitivity_risk": highest_sensitivity_risk,
        "sensitivity_next_move": sensitivity_next_move,
        "cash_flow_series": load_cash_flow_series(),
    }


def render_metric_card(title, value, caption, color_class=""):
    st.markdown(
        f"""
        <div class="bos-card">
            <div class="bos-card-title">{title}</div>
            <div class="bos-card-value {color_class}">{value}</div>
            <div class="bos-card-caption">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_panel_start(title):
    st.markdown(
        f"""
        <div class="bos-panel">
            <div class="bos-section-title">{title}</div>
        """,
        unsafe_allow_html=True,
    )


def render_panel_end():
    st.markdown("</div>", unsafe_allow_html=True)


def render_brief_item(main_text, sub_text):
    st.markdown(
        f"""
        <div class="bos-brief-item">
            <div class="bos-dot"></div>
            <div>
                <div class="bos-item-main">{main_text}</div>
                <div class="bos-item-sub">{sub_text}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status_row(title, subtitle, status):
    status_class = str(status).lower().replace("_", "-")
    if status_class == "critical":
        status_class = "high"

    st.markdown(
        f"""
        <div class="bos-row">
            <div>
                <div class="bos-item-main">{title}</div>
                <div class="bos-item-sub">{subtitle}</div>
            </div>
            <div class="bos-badge {status_class}">{status}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_login():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown('<div class="bos-login-card">', unsafe_allow_html=True)
    st.title("BusinessOS")
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

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


def render_sidebar():
    role = st.session_state.get("role", "viewer")
    username = st.session_state.get("username", "user")
    allowed_pages = get_allowed_pages(role)

    st.sidebar.title("BusinessOS")
    st.sidebar.caption("Intelligence for better decisions")
    st.sidebar.divider()
    page = st.sidebar.radio("Navigation", allowed_pages)
    st.sidebar.divider()
    st.sidebar.caption(f"Signed in as {username}")
    st.sidebar.caption(f"Role: {role}")

    if st.sidebar.button("Refresh", use_container_width=True):
        st.rerun()

    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    return page


def render_dashboard(data):
    st.markdown(
        f"""
        <div class="bos-topbar">
            <div>
                <div class="bos-title">BusinessOS Command Center</div>
                <div class="bos-subtitle">Unified executive intelligence across Finance, Operations, Governance, Sensitivity, Support, Assistance, and People.</div>
            </div>
            <div class="bos-chip">System Health: {data['overall_health']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card("Financial Health", data["overall_health"], f"Net cash flow ${data['net_cash_flow']:,.2f}", data["health_class"])
    with col2:
        render_metric_card("Open Risks", data["highest_risk"], f"{data['overdue_operations_tasks']} overdue operations task(s)", "red")
    with col3:
        render_metric_card("Pending Actions", data["active_finance_actions"], "Requires executive review", "gold")
    with col4:
        render_metric_card("Critical Incidents", data["active_support_incidents"], "Active support workload", "red")

    left, right = st.columns([1, 1.95])

    with left:
        render_panel_start("Executive Brief")
        render_brief_item(data["next_move"], "Recommended cross-module executive move")
        render_brief_item(
            f"{data['active_finance_actions']} finance action(s) are active",
            "Finance intelligence remains in execution mode",
        )
        render_brief_item(
            f"{data['overdue_operations_tasks']} overdue operations task(s)",
            "Operations needs follow-up before workload expansion",
        )
        render_brief_item(
            f"{data['active_support_incidents']} support incident(s) active",
            "Support investigation is part of current system risk",
        )
        render_brief_item(
            f"{data['active_assistance_requests']} assistance request(s) active",
            "Internal users are asking BusinessOS for help, decisions, or routing",
        )
        render_panel_end()

    with right:
        render_panel_start("Cash Flow Overview")
        if data["cash_flow_series"].empty:
            st.info("No cash flow data available yet.")
        else:
            st.area_chart(data["cash_flow_series"], x="date", y="net_cash_flow", height=285)
        render_panel_end()

    ops_col, incident_col, alert_col = st.columns(3)

    with ops_col:
        render_panel_start("Operations Overview")
        if data["active_tasks"]:
            for task in data["active_tasks"]:
                render_status_row(task["title"], f"{task['owner_role']} | {task['status']}", task["priority"])
        else:
            render_status_row("No active operations tasks", "Operations workload is clear", "healthy")
        render_panel_end()

    with incident_col:
        render_panel_start("Recent Incidents")
        if data["recent_incidents"]:
            for incident in data["recent_incidents"]:
                render_status_row(incident["title"], f"{incident['owner_role']} | {incident['status']}", incident["severity"])
        else:
            render_status_row("No active incidents", "Support queue is clear", "healthy")
        render_panel_end()

    with alert_col:
        render_panel_start("Alerts")
        render_status_row("Expense concentration", "Marketing expenses require review", "high")
        render_status_row("Operations follow-up", "One task is overdue", "high" if data["overdue_operations_tasks"] else "low")
        render_status_row("Governance posture", "Audit trail health remains healthy", "low")
        render_panel_end()


def render_module_page(page, data):
    st.markdown(
        f"""
        <div class="bos-topbar">
            <div>
                <div class="bos-title">{page}</div>
                <div class="bos-subtitle">Focused module view from the current BusinessOS dataset.</div>
            </div>
            <div class="bos-chip">Access: {st.session_state.get('role', 'viewer')}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if page == "Finance":
        c1, c2, c3 = st.columns(3)
        with c1:
            render_metric_card("Transactions", data["transactions_count"], "Loaded records", "")
        with c2:
            render_metric_card("Income", f"${data['total_income']:,.2f}", "Current sample dataset", "green")
        with c3:
            render_metric_card("Expenses", f"${data['total_expenses']:,.2f}", "Current sample dataset", "red")

    elif page == "Operations":
        c1, c2 = st.columns(2)
        with c1:
            render_metric_card("Active Tasks", data["active_operations_tasks"], "Open, in progress, or blocked", "gold")
        with c2:
            render_metric_card("Overdue Tasks", data["overdue_operations_tasks"], "Needs owner follow-up", "red")

    elif page == "Governance":
        c1, c2 = st.columns(2)
        with c1:
            render_metric_card("Governance Findings", data["governance_findings"], "Detected from audit logs", "green")
        with c2:
            render_metric_card("Error/Critical Events", data["error_events"], "Audit severity monitor", "green")

    elif page == "Support":
        c1, c2 = st.columns(2)
        with c1:
            render_metric_card("Active Incidents", data["active_support_incidents"], "Open, investigating, or waiting", "red")
        with c2:
            render_metric_card("Critical/High Incidents", data["critical_support_incidents"], "Escalation-sensitive queue", "gold")

    elif page == "Assistance":
        c1, c2, c3 = st.columns(3)
        with c1:
            render_metric_card("Active Requests", data["active_assistance_requests"], "Open, triaged, approval, or in progress", "gold")
        with c2:
            render_metric_card("High-Severity Requests", data["high_assistance_requests"], "Requires owner attention", "red")
        with c3:
            render_metric_card("Waiting Approval", data["waiting_approval_requests"], "Blocked on approval", "gold")

        left, right = st.columns([1.4, 1])

        with left:
            render_panel_start("Active Assistance Requests")
            if data["assistance_requests"]:
                for request in data["assistance_requests"]:
                    render_status_row(
                        request["title"],
                        f"{request['owner_role']} | {request['request_type']} | {request['status']}",
                        request["severity"],
                    )
            else:
                render_status_row("No active assistance requests", "Internal request queue is clear", "healthy")
            render_panel_end()

        with right:
            render_panel_start("Assistance Brief")
            render_brief_item(
                f"{data['active_assistance_requests']} active assistance request(s)",
                "Internal work is now visible as request flow",
            )
            render_brief_item(
                f"{data['high_assistance_requests']} high-severity request(s)",
                "Prioritize owner assignment and triage",
            )
            render_brief_item(
                f"{data['waiting_approval_requests']} waiting for approval",
                "Governance-sensitive requests should not bypass review",
            )
            render_panel_end()

    elif page == "People":
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            render_metric_card("Total Users", data["total_people"], "Registered internal users", "")
        with c2:
            render_metric_card("Active Users", data["active_people"], "Currently enabled", "green")
        with c3:
            render_metric_card("Admin Users", data["admin_people"], "Maximum access level", "red")
        with c4:
            render_metric_card("Managers", data["manager_people"], "Department leadership", "gold")

        left, right = st.columns([1.5, 1])

        with left:
            render_panel_start("People Directory")
            if data["people_users"]:
                for user in data["people_users"]:
                    render_status_row(
                        user["full_name"],
                        f"{user['department']} | {user['role']} | {user['email']}",
                        user["access_level"],
                    )
            else:
                render_status_row("No users found", "People directory has not been initialized", "healthy")
            render_panel_end()

        with right:
            render_panel_start("People Brief")
            render_brief_item(
                f"{data['active_people']} active user(s)",
                "BusinessOS has an initialized internal user layer",
            )
            render_brief_item(
                f"{data['admin_people']} admin user(s)",
                "Admin coverage protects institutional control",
            )
            render_brief_item(
                f"{data['manager_people']} manager user(s)",
                "Managers are ready for routing, approvals, and ownership",
            )
            render_panel_end()

    elif page == "Sensitivity":
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            render_metric_card("Sensitive Findings", data["sensitive_findings"], "Signals requiring institutional control", "gold")
        with c2:
            render_metric_card("High Sensitivity", data["high_sensitivity_findings"], "Needs executive attention", "red")
        with c3:
            render_metric_card("Medium Sensitivity", data["medium_sensitivity_findings"], "Needs owner review", "gold")
        with c4:
            render_metric_card("Highest Risk", data["highest_sensitivity_risk"], "Governance sensitivity level", "red" if data["highest_sensitivity_risk"] == "High" else "gold")

        left, right = st.columns([1.55, 1])

        with left:
            render_panel_start("Sensitivity Findings")
            if data["sensitivity_findings"]:
                for finding in data["sensitivity_findings"][:8]:
                    render_status_row(
                        finding["message"],
                        f"{finding['source']} | {finding['finding_type']}",
                        finding["severity"],
                    )
            else:
                render_status_row("No sensitive findings", "Governance sensitivity controls are clear", "healthy")
            render_panel_end()

        with right:
            render_panel_start("Sensitivity Brief")
            render_brief_item(
                f"{data['sensitive_findings']} sensitive finding(s)",
                "BusinessOS is actively classifying institutional sensitivity",
            )
            render_brief_item(
                f"{data['high_sensitivity_findings']} high-sensitivity finding(s)",
                "High findings should be reviewed before dependent actions proceed",
            )
            render_brief_item(
                data["sensitivity_next_move"],
                "Recommended governance sensitivity move",
            )
            render_panel_end()

def main():
    st.set_page_config(
        page_title="BusinessOS Command Center",
        page_icon="B",
        layout="wide",
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    if not st.session_state.get("authenticated"):
        render_login()

    page = render_sidebar()
    data = load_dashboard_data()

    if page == "Dashboard":
        render_dashboard(data)
    else:
        render_module_page(page, data)


if __name__ == "__main__":
    main()



