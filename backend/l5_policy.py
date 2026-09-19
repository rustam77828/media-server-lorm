import subprocess
import json
import os
from datetime import datetime

POLICIES_FILE = os.path.join(os.path.dirname(__file__), "policies.json")
EVENTS_FILE = os.path.join(os.path.dirname(__file__), "policy_events.log")

DEFAULT_POLICIES = [
    {
        "id": "disk_high",
        "name": "Disk usage above 90%",
        "condition": "disk_usage > 90",
        "action": "notify",
        "enabled": True,
        "author": "admin",
        "created": "2026-09-19",
        "expires": "2027-09-19"
    },
    {
        "id": "temp_high",
        "name": "CPU temperature above 80°C",
        "condition": "cpu_temp > 80",
        "action": "notify",
        "enabled": True,
        "author": "admin",
        "created": "2026-09-19",
        "expires": "2027-09-19"
    },
    {
        "id": "uptime_long",
        "name": "Uptime above 60 days",
        "condition": "uptime_days > 60",
        "action": "recommend_reboot",
        "enabled": True,
        "author": "admin",
        "created": "2026-09-19",
        "expires": "2027-09-19"
    }
]

def load_policies():
    if not os.path.exists(POLICIES_FILE):
        with open(POLICIES_FILE, "w") as f:
            json.dump(DEFAULT_POLICIES, f, indent=2, ensure_ascii=False)
        return DEFAULT_POLICIES
    with open(POLICIES_FILE, "r") as f:
        return json.load(f)

def log_event(policy_id, triggered, details):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "policy_id": policy_id,
        "triggered": triggered,
        "details": details
    }
    with open(EVENTS_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry

def check_disk_usage():
    result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")
    if len(lines) < 2:
        return 0
    usage = lines[1].split()[4].replace("%", "")
    try:
        return int(usage)
    except ValueError:
        return 0

def check_cpu_temp():
    result = subprocess.run(["sensors"], capture_output=True, text=True)
    for line in result.stdout.split("\n"):
        if "Package id 0" in line or "Core 0" in line:
            for part in line.split():
                if "+" in part and "°C" in part:
                    try:
                        return float(part.replace("+", "").replace("°C", ""))
                    except ValueError:
                        pass
    return 0

def check_uptime_days():
    result = subprocess.run(["uptime", "-p"], capture_output=True, text=True)
    output = result.stdout.strip()
    days = 0
    for word in output.split():
        if word.isdigit():
            days = int(word)
            break
    if "day" in output:
        parts = output.split()
        for i, word in enumerate(parts):
            if word == "day" or word == "days":
                if i > 0 and parts[i-1].isdigit():
                    days = int(parts[i-1])
                break
    return days

def evaluate_policies():
    policies = load_policies()
    results = []
    disk = check_disk_usage()
    temp = check_cpu_temp()
    uptime = check_uptime_days()

    for policy in policies:
        triggered = False
        details = ""

        if policy["id"] == "disk_high":
            triggered = disk > 90
            details = f"Disk usage: {disk}%"
        elif policy["id"] == "temp_high":
            triggered = temp > 80
            details = f"CPU temp: {temp}°C"
        elif policy["id"] == "uptime_long":
            triggered = uptime > 60
            details = f"Uptime: {uptime} days"

        if triggered:
            log_event(policy["id"], True, details)

        results.append({
            "policy": policy["name"],
            "enabled": policy["enabled"],
            "triggered": triggered,
            "details": details,
            "action": policy["action"],
            "expires": policy["expires"]
        })

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "policies": results
    }

def get_policy_events(limit=20):
    if not os.path.exists(EVENTS_FILE):
        return []
    with open(EVENTS_FILE, "r") as f:
        lines = f.readlines()
    return [json.loads(line) for line in lines[-limit:]]

if __name__ == "__main__":
    print(json.dumps(evaluate_policies(), indent=2, ensure_ascii=False))
