import subprocess
import json
from datetime import datetime

def get_uptime():
    result = subprocess.run(["uptime", "-p"], capture_output=True, text=True)
    return result.stdout.strip()

def get_load_average():
    result = subprocess.run(["uptime"], capture_output=True, text=True)
    return result.stdout.strip()

def get_memory():
    result = subprocess.run(["free", "-h"], capture_output=True, text=True)
    return result.stdout

def get_disk_usage():
    result = subprocess.run(["df", "-h"], capture_output=True, text=True)
    return result.stdout

def get_temperature():
    result = subprocess.run(["sensors"], capture_output=True, text=True)
    if result.returncode != 0:
        return "sensors not available"
    return result.stdout

def get_docker_stats():
    result = subprocess.run(
        ["docker", "stats", "--no-stream", "--format",
         "{{.Name}}|{{.CPUPerc}}|{{.MemUsage}}|{{.NetIO}}|{{.BlockIO}}"],
        capture_output=True, text=True
    )
    return result.stdout

def get_boot_history():
    result = subprocess.run(["journalctl", "--list-boots"], capture_output=True, text=True)
    return result.stdout

def get_auth_log():
    result = subprocess.run(
        ["sudo", "tail", "-20", "/var/log/auth.log"],
        capture_output=True, text=True
    )
    return result.stdout

def collect_metrics():
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": get_uptime(),
        "load_average": get_load_average(),
        "memory": get_memory(),
        "disk_usage": get_disk_usage(),
        "temperature": get_temperature(),
        "docker_stats": get_docker_stats(),
        "boot_history": get_boot_history(),
        "auth_log": get_auth_log(),
    }

if __name__ == "__main__":
    metrics = collect_metrics()
    print(json.dumps(metrics, indent=2, ensure_ascii=False))
