import argparse
import subprocess
import sys
import time


QUICK_COMMANDS = [
    "health",
    "system-check",
    "release-readiness",
    "runtime-stability",
    "notifications",
    "ops-brief",
    "gov-brief",
    "support-brief",
    "command-center",
    "daily-close-schedule",
]

PILOT_CHAIN_COMMANDS = [
    "private-demo-dry-run",
    "private-pilot-intake",
    "private-pilot-plan",
    "private-pilot-tracker",
    "private-pilot-exit-decision",
    "pilot-day-1-package",
    "pilot-day-2-rhythm",
    "pilot-day-3-evidence-review",
    "pilot-day-4-owner-confirmation",
    "pilot-day-5-narrow-continuation",
    "pilot-expansion-review-prep",
    "pilot-expansion-review-decision",
    "pilot-expansion-approval-gate-prep",
    "pilot-expansion-approval-request-draft",
]

STANDARD_COMMANDS = [
    "health",
    "system-check",
    "actions",
    "finance-area-review",
    "reports",
    "area-review-index",
    "area-review-bundle",
    "release-readiness",
    "runtime-stability",
    "public-surface-publish-checklist",
    "private-demo-package",
    "private-demo-script",
    "ops-tasks",
    "ops-escalations",
    "ops-brief",
    "operations-area-review",
    "gov-findings",
    "gov-kpis",
    "gov-brief",
    "gov-report",
    "gov-sensitivity",
    "gov-sensitivity-brief",
    "governance-area-review",
    "support-incidents",
    "support-brief",
    "support-report",
    "support-area-review",
    "command-center",
    "command-report",
    "people",
    "people-brief",
    "assistance",
    "assistance-brief",
    "assistance-status",
    "approvals",
    "approval-brief",
    "approval-report",
    "approval-approve",
    "approval-reject",
    "evidence-index",
    "executive-alerts",
    "executive-alerts-brief",
    "executive-alerts-report",
    "executive-alert-status",
    "executive-alert-review",
    "executive-alert-resolve",
    "daily-close",
    "daily-close-distribution",
    "notification-delivery-approval",
    "secure-email-delivery",
    "daily-close-schedule",
    "scheduled-daily-close",
    "notification-sent",
    "notification-dismiss",
    "notification-fail",
    "notifications",
    "run",
]

FULL_COMMANDS = [
    "health",
    "system-check",
    "actions",
    "finance-area-review",
    "reports",
    "area-review-index",
    "area-review-bundle",
    "release-readiness",
    "runtime-stability",
    "public-surface-publish-checklist",
    "private-demo-package",
    "private-demo-script",
    *PILOT_CHAIN_COMMANDS,
    "ops-tasks",
    "ops-escalations",
    "ops-brief",
    "operations-area-review",
    "gov-findings",
    "gov-kpis",
    "gov-brief",
    "gov-report",
    "gov-sensitivity",
    "gov-sensitivity-brief",
    "governance-area-review",
    "support-incidents",
    "support-brief",
    "support-report",
    "support-area-review",
    "command-center",
    "command-report",
    "people",
    "people-brief",
    "assistance",
    "assistance-brief",
    "assistance-status",
    "approvals",
    "approval-brief",
    "approval-report",
    "approval-approve",
    "approval-reject",
    "evidence-index",
    "executive-alerts",
    "executive-alerts-brief",
    "executive-alerts-report",
    "executive-alert-status",
    "executive-alert-review",
    "executive-alert-resolve",
    "daily-close",
    "daily-close-distribution",
    "notification-delivery-approval",
    "secure-email-delivery",
    "daily-close-schedule",
    "scheduled-daily-close",
    "notification-sent",
    "notification-dismiss",
    "notification-fail",
    "notifications",
    "run",
]

PROFILES = {
    "quick": QUICK_COMMANDS,
    "standard": STANDARD_COMMANDS,
    "full": FULL_COMMANDS,
}

# Backward-compatible default used by runtime review tooling.
COMMANDS = STANDARD_COMMANDS


def build_command(command_name):
    return [sys.executable, "cli.py", command_name]


def run_command(command_name, timeout_seconds):
    command = build_command(command_name)
    display_command = f"python cli.py {command_name}"
    print(f"Running: {display_command}")

    start_time = time.perf_counter()
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as error:
        duration = time.perf_counter() - start_time
        print(error.stdout or "")
        print(error.stderr or "")
        print(f"[FAILED] {display_command} timed out after {duration:.2f}s")
        return False

    duration = time.perf_counter() - start_time

    if result.stdout:
        print(result.stdout)

    if result.stderr:
        print(result.stderr)

    if result.returncode != 0:
        print(f"[FAILED] {display_command} ({duration:.2f}s)")
        return False

    print(f"[PASSED] {display_command} ({duration:.2f}s)")
    return True


def parse_args():
    parser = argparse.ArgumentParser(description="BusinessOS smoke test runner")
    parser.add_argument(
        "profile",
        nargs="?",
        default="standard",
        choices=sorted(PROFILES),
        help="Smoke profile to run. Default: standard.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Per-command timeout in seconds. Default: 300.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    commands = PROFILES[args.profile]

    print("BusinessOS Smoke Test")
    print(f"Profile: {args.profile}")
    print(f"Commands: {len(commands)}")
    print(f"Per-command timeout: {args.timeout}s")

    all_passed = True

    for command_name in commands:
        if not run_command(command_name, args.timeout):
            all_passed = False
            break

    if not all_passed:
        print("Smoke test failed.")
        sys.exit(1)

    print("Smoke test completed successfully.")


if __name__ == "__main__":
    main()
