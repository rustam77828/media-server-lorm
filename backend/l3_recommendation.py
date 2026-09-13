import subprocess
import json
from datetime import datetime

def recommend_reboot():
    result = subprocess.run(["uname", "-r"], capture_output=True, text=True)
    running = result.stdout.strip()
    result = subprocess.run(
        ["apt", "list", "--upgradable"],
        capture_output=True, text=True
    )
    if "linux-image" in result.stdout:
        return {
            "action": "reboot",
            "reason": f"Running kernel {running} is outdated",
            "risk": "medium",
            "expected_result": "New kernel loaded, security patches active",
            "rollback": "Not possible (kernel upgrade is one-way)",
            "alternatives": [
                "Schedule reboot during maintenance window",
                "Do nothing (system continues with old kernel)"
            ],
            "requires_approval": True
        }
    return None

def recommend_cleanup_logs():
    result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")
    if len(lines) < 2:
        return None
    parts = lines[1].split()
    usage = parts[4].replace("%", "")
    try:
        usage_int = int(usage)
    except ValueError:
        return None
    if usage_int > 70:
        return {
            "action": "cleanup_logs",
            "reason": f"Disk usage at {usage}%",
            "risk": "low",
            "expected_result": "Free up disk space",
            "rollback": "Not possible (logs are deleted)",
            "alternatives": [
                "Archive logs to external storage",
                "Do nothing (disk still has free space)"
            ],
            "requires_approval": True
        }
    return None

def recommend_gpu_driver():
    result = subprocess.run(["sensors"], capture_output=True, text=True)
    if "nouveau" in result.stdout and "65" in result.stdout:
        return {
            "action": "replace_gpu_driver",
            "reason": "GPU temperature 65°C with nouveau driver",
            "risk": "high",
            "expected_result": "Lower GPU temperature (5-10°C)",
            "rollback": "Reinstall nouveau (requires reboot)",
            "alternatives": [
                "Improve cooling (fan, thermal paste)",
                "Do nothing (65°C is within safe range)"
            ],
            "requires_approval": True
        }
    return None

def collect_recommendations():
    recommendations = []
    for func in [recommend_reboot, recommend_cleanup_logs, recommend_gpu_driver]:
        rec = func()
        if rec:
            recommendations.append(rec)
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "recommendations": recommendations
    }

if __name__ == "__main__":
    print(json.dumps(collect_recommendations(), indent=2, ensure_ascii=False))
