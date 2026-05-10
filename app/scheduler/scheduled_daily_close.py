from datetime import date, datetime
from pathlib import Path

from app.audit.audit_log import write_audit_log


ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"
DEFAULT_SCHEDULE_NAME = "executive_daily_close"
DEFAULT_RUN_TIME_LOCAL = "18:00"


def create_scheduled_daily_close_table(conn):
    query = """
    CREATE TABLE IF NOT EXISTS scheduled_daily_close (
        schedule_name TEXT PRIMARY KEY,
        enabled INTEGER NOT NULL,
        run_time_local TEXT NOT NULL,
        last_run_date TEXT,
        last_started_at TEXT,
        last_completed_at TEXT,
        last_status TEXT,
        last_message TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """
    conn.execute(query)
    conn.commit()


def ensure_default_scheduled_daily_close(conn):
    create_scheduled_daily_close_table(conn)

    existing = conn.execute(
        """
        SELECT schedule_name
        FROM scheduled_daily_close
        WHERE schedule_name = ?
        LIMIT 1
        """,
        (DEFAULT_SCHEDULE_NAME,),
    ).fetchone()

    if existing:
        return

    now = datetime.now().isoformat()
    conn.execute(
        """
        INSERT INTO scheduled_daily_close (
            schedule_name,
            enabled,
            run_time_local,
            last_run_date,
            last_started_at,
            last_completed_at,
            last_status,
            last_message,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            DEFAULT_SCHEDULE_NAME,
            1,
            DEFAULT_RUN_TIME_LOCAL,
            None,
            None,
            None,
            "ready",
            "Default scheduled daily close initialized.",
            now,
            now,
        ),
    )
    conn.commit()

    write_audit_log(
        conn,
        "scheduled_daily_close_initialized",
        "info",
        "Scheduled daily close initialized.",
        {
            "schedule_name": DEFAULT_SCHEDULE_NAME,
            "run_time_local": DEFAULT_RUN_TIME_LOCAL,
        },
    )


def _get_schedule(conn):
    ensure_default_scheduled_daily_close(conn)
    row = conn.execute(
        """
        SELECT
            schedule_name,
            enabled,
            run_time_local,
            last_run_date,
            last_started_at,
            last_completed_at,
            last_status,
            last_message
        FROM scheduled_daily_close
        WHERE schedule_name = ?
        LIMIT 1
        """,
        (DEFAULT_SCHEDULE_NAME,),
    ).fetchone()

    return {
        "schedule_name": row[0],
        "enabled": bool(row[1]),
        "run_time_local": row[2],
        "last_run_date": row[3],
        "last_started_at": row[4],
        "last_completed_at": row[5],
        "last_status": row[6],
        "last_message": row[7],
    }


def _today_report_exists(run_date):
    report_path = REPORTS_DIR / f"daily_close_{run_date}.md"
    return report_path.exists(), str(report_path.relative_to(ROOT_DIR))


def _is_at_or_after_run_time(now, run_time_local):
    current_time = now.strftime("%H:%M")
    return current_time >= run_time_local


def get_scheduled_daily_close_status(conn, now=None):
    current_time = now or datetime.now()
    current_date = current_time.date().isoformat()
    schedule = _get_schedule(conn)
    report_exists, report_path = _today_report_exists(current_date)

    if not schedule["enabled"]:
        next_action = "disabled"
    elif schedule["last_run_date"] == current_date:
        next_action = "already_recorded_today"
    elif report_exists:
        next_action = "close_already_available"
    elif not _is_at_or_after_run_time(current_time, schedule["run_time_local"]):
        next_action = "waiting_for_run_time"
    else:
        next_action = "due"

    return {
        **schedule,
        "today": current_date,
        "current_time_local": current_time.strftime("%H:%M"),
        "today_report_exists": report_exists,
        "today_report_path": report_path,
        "next_action": next_action,
    }


def _record_schedule_result(conn, status, message, run_date=None, started_at=None):
    now = datetime.now().isoformat()
    conn.execute(
        """
        UPDATE scheduled_daily_close
        SET last_run_date = ?,
            last_started_at = COALESCE(?, last_started_at),
            last_completed_at = ?,
            last_status = ?,
            last_message = ?,
            updated_at = ?
        WHERE schedule_name = ?
        """,
        (
            run_date or date.today().isoformat(),
            started_at,
            now,
            status,
            message,
            now,
            DEFAULT_SCHEDULE_NAME,
        ),
    )
    conn.commit()


def run_scheduled_daily_close(conn, daily_close_callback, now=None):
    status = get_scheduled_daily_close_status(conn, now=now)
    run_date = status["today"]

    if status["next_action"] == "disabled":
        message = "Scheduled Daily Close skipped: schedule is disabled."
        print(message)
        return {**status, "run_status": "skipped", "message": message}

    if status["next_action"] == "waiting_for_run_time":
        message = (
            "Scheduled Daily Close skipped: "
            f"waiting for {status['run_time_local']} local time."
        )
        print(message)
        return {**status, "run_status": "skipped", "message": message}

    if status["next_action"] == "already_recorded_today":
        message = "Scheduled Daily Close skipped: schedule already recorded today's close."
        print(message)
        return {**status, "run_status": "skipped", "message": message}

    if status["next_action"] == "close_already_available":
        message = f"Scheduled Daily Close skipped: {status['today_report_path']} already exists."
        _record_schedule_result(conn, "skipped_existing_close", message, run_date=run_date)
        write_audit_log(
            conn,
            "scheduled_daily_close_skipped",
            "info",
            "Scheduled daily close skipped because today's close already exists.",
            {"report_path": status["today_report_path"], "run_date": run_date},
        )
        print(message)
        return {**status, "run_status": "skipped", "message": message}

    started_at = datetime.now().isoformat()
    conn.execute(
        """
        UPDATE scheduled_daily_close
        SET last_started_at = ?,
            last_status = ?,
            last_message = ?,
            updated_at = ?
        WHERE schedule_name = ?
        """,
        (
            started_at,
            "running",
            "Scheduled daily close started.",
            started_at,
            DEFAULT_SCHEDULE_NAME,
        ),
    )
    conn.commit()

    write_audit_log(
        conn,
        "scheduled_daily_close_started",
        "info",
        "Scheduled daily close started.",
        {"run_date": run_date},
    )

    try:
        daily_close_callback()
    except Exception as error:
        message = f"Scheduled Daily Close failed: {error}"
        _record_schedule_result(
            conn,
            "failed",
            message,
            run_date=run_date,
            started_at=started_at,
        )
        write_audit_log(
            conn,
            "scheduled_daily_close_failed",
            "error",
            "Scheduled daily close failed.",
            {"run_date": run_date, "error": str(error)},
        )
        raise

    message = "Scheduled Daily Close completed."
    _record_schedule_result(
        conn,
        "completed",
        message,
        run_date=run_date,
        started_at=started_at,
    )
    write_audit_log(
        conn,
        "scheduled_daily_close_completed",
        "info",
        "Scheduled daily close completed.",
        {"run_date": run_date},
    )
    print(message)
    return {**status, "run_status": "completed", "message": message}


def print_scheduled_daily_close_status(conn):
    status = get_scheduled_daily_close_status(conn)

    print("Scheduled Daily Close:")
    print(f"Schedule: {status['schedule_name']}")
    print(f"Enabled: {'yes' if status['enabled'] else 'no'}")
    print(f"Run time local: {status['run_time_local']}")
    print(f"Today: {status['today']}")
    print(f"Current local time: {status['current_time_local']}")
    print(f"Today report exists: {'yes' if status['today_report_exists'] else 'no'}")
    print(f"Today report path: {status['today_report_path']}")
    print(f"Last run date: {status['last_run_date'] or 'none'}")
    print(f"Last status: {status['last_status'] or 'none'}")
    print(f"Next action: {status['next_action']}")

    write_audit_log(
        conn,
        "scheduled_daily_close_viewed",
        "info",
        "Scheduled daily close status viewed.",
        {
            "next_action": status["next_action"],
            "last_status": status["last_status"],
            "today_report_exists": status["today_report_exists"],
        },
    )

    return status
