import subprocess
import json
import os
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "actions.log")

def log_action(action, status, details=""):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "action": action,
        "status": status,
        "details": details
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry

def action_cleanup_logs(confirm):
    if not confirm:
        return {
            "action": "cleanup_logs",
            "status": "rejected",
            "message": "Approval required"
        }
    result = subprocess.run(
        ["journalctl", "--disk-usage"],
        capture_output=True, text=True
    )
    log_action("cleanup_logs", "executed", result.stdout.strip())
    return {
        "action": "cleanup_logs",
        "status": "executed",
        "output": result.stdout.strip(),
        "message": "Log usage checked. Run 'sudo journalctl --vacuum-time=7d' manually to clean."
    }

def action_update_packages(confirm):
    if not confirm:
        return {
            "action": "update_packages",
            "status": "rejected",
            "message": "Approval required"
        }
    result = subprocess.run(
        ["apt", "list", "--upgradable"],
        capture_output=True, text=True
    )
    lines = [l for l in result.stdout.split("\n") if "/" in l]
    count = len(lines)
    log_action("update_packages", "executed", f"{count} packages pending")
    return {
        "action": "update_packages",
        "status": "executed",
        "output": f"{count} packages available for update",
        "message": f"{count} packages pending. Run 'sudo apt upgrade' manually."
    }

def action_reboot(confirm):
    if not confirm:
        return {
            "action": "reboot",
            "status": "rejected",
            "message": "Approval required"
        }
    log_action("reboot", "scheduled", "Reboot would be scheduled")
    return {
        "action": "reboot",
        "status": "scheduled",
        "message": "Reboot approved. Run 'sudo reboot' manually to execute."
    }

ACTIONS = {
    "cleanup_logs": action_cleanup_logs,
    "update_packages": action_update_packages,
    "reboot": action_reboot,
}

def execute_action(action_name, confirm=False):
    if action_name not in ACTIONS:
        return {
            "action": action_name,
            "status": "error",
            "message": f"Unknown action. Available: {list(ACTIONS.keys())}"
        }
    return ACTIONS[action_name](confirm)

def get_action_history(limit=20):
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
    return [json.loads(line) for line in lines[-limit:]]

if __name__ == "__main__":
    print(json.dumps(execute_action("cleanup_logs", confirm=False), indent=2, ensure_ascii=False))
