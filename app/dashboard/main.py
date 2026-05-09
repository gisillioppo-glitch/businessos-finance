import sqlite3

import streamlit as st

DB_PATH = "finance.db"


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


def main():
    st.set_page_config(
        page_title="BusinessOS Command Center",
        page_icon="B",
        layout="wide",
    )

    st.sidebar.title("BusinessOS")
    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Finance",
            "Operations",
            "Governance",
            "Support",
        ],
    )

    if st.sidebar.button("Refresh"):
        st.rerun()

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
