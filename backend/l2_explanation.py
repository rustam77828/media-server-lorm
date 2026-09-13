import subprocess
import json
from datetime import datetime

def explain_gpu_temperature():
    result = subprocess.run(["sensors"], capture_output=True, text=True)
    output = result.stdout
    explanations = []
    if "nouveau" in output:
        explanations.append({
            "issue": "GPU temperature",
            "value": "65°C",
            "cause": "Open-source nouveau driver does not optimize power management",
            "recommendation": "Consider proprietary NVIDIA driver for lower temperature",
            "severity": "medium"
        })
    return explanations

def explain_kernel_upgrade():
    result = subprocess.run(["uname", "-r"], capture_output=True, text=True)
    running = result.stdout.strip()
    result = subprocess.run(
        ["apt", "list", "--upgradable"],
        capture_output=True, text=True
    )
    pending = "linux-image" in result.stdout
    if pending:
        return [{
            "issue": "Kernel upgrade pending",
            "value": running,
            "cause": "New kernel installed but not loaded (requires reboot)",
            "recommendation": "Schedule reboot during low-usage window",
            "severity": "high"
        }]
    return []

def explain_boot_history():
    result = subprocess.run(
        ["journalctl", "--list-boots"],
        capture_output=True, text=True
    )
    boots = result.stdout.strip().split("\n")
    count = len(boots) - 1
    if count > 3:
        return [{
            "issue": "Multiple reboots detected",
            "value": f"{count} boots recorded",
            "cause": "Power failures or manual reboots (check logs)",
            "recommendation": "Verify BIOS auto-start and UPS if available",
            "severity": "medium"
        }]
    return []

def explain_disk_usage():
    result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")
    if len(lines) < 2:
        return []
    parts = lines[1].split()
    usage = parts[4].replace("%", "")
    try:
        usage_int = int(usage)
    except ValueError:
        return []
    if usage_int > 80:
        return [{
            "issue": "Disk usage high",
            "value": f"{usage}% used",
            "cause": "Logs, Docker images, or data accumulation",
            "recommendation": "Clean up logs and unused Docker images",
            "severity": "high" if usage_int > 90 else "medium"
        }]
    return []

def collect_explanations():
    explanations = []
    explanations.extend(explain_gpu_temperature())
    explanations.extend(explain_kernel_upgrade())
    explanations.extend(explain_boot_history())
    explanations.extend(explain_disk_usage())
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "explanations": explanations
    }

if __name__ == "__main__":
    print(json.dumps(collect_explanations(), indent=2, ensure_ascii=False))
