import subprocess
import sys


COMMANDS = [
    ["python", "cli.py", "health"],
    ["python", "cli.py", "actions"],
    ["python", "cli.py", "reports"],
    ["python", "cli.py", "ops-tasks"],
    ["python", "cli.py", "ops-escalations"],
    ["python", "cli.py", "ops-brief"],
    ["python", "cli.py", "gov-findings"],
    ["python", "cli.py", "gov-kpis"],
    ["python", "cli.py", "gov-brief"],
    ["python", "cli.py", "gov-report"],
    ["python", "cli.py", "gov-sensitivity"],
    ["python", "cli.py", "gov-sensitivity-brief"],
    ["python", "cli.py", "support-incidents"],
    ["python", "cli.py", "support-brief"],
    ["python", "cli.py", "support-report"],
    ["python", "cli.py", "command-center"],
    ["python", "cli.py", "command-report"],
    ["python", "cli.py", "people"],
    ["python", "cli.py", "people-brief"],
    ["python", "cli.py", "assistance"],
    ["python", "cli.py", "assistance-brief"],
    ["python", "cli.py", "assistance-status"],
    ["python", "cli.py", "approvals"],
    ["python", "cli.py", "approval-brief"],
    ["python", "cli.py", "executive-alerts"],
    ["python", "cli.py", "executive-alerts-brief"],
    ["python", "cli.py", "run"],
]


def run_command(command):
    print(f"Running: {' '.join(command)}")

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )

    if result.stdout:
        print(result.stdout)

    if result.stderr:
        print(result.stderr)

    if result.returncode != 0:
        print(f"[FAILED] {' '.join(command)}")
        return False

    print(f"[PASSED] {' '.join(command)}")
    return True


def main():
    print("BusinessOS Smoke Test")

    all_passed = True

    for command in COMMANDS:
        if not run_command(command):
            all_passed = False
            break

    if not all_passed:
        print("Smoke test failed.")
        sys.exit(1)

    print("Smoke test completed successfully.")


if __name__ == "__main__":
    main()







