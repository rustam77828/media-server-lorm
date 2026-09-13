import subprocess
import json

def get_disks():
    result = subprocess.run(["df", "-h"], capture_output=True, text=True)
    return result.stdout

def get_block_devices():
    result = subprocess.run(["lsblk"], capture_output=True, text=True)
    return result.stdout

def get_docker_containers():
    result = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}|{{.Image}}|{{.Status}}"],
        capture_output=True, text=True
    )
    return result.stdout

def get_docker_images():
    result = subprocess.run(
        ["docker", "images", "--format", "{{.Repository}}:{{.Tag}}"],
        capture_output=True, text=True
    )
    return result.stdout

def get_services():
    result = subprocess.run(
        ["systemctl", "list-units", "--type=service", "--state=running", "--no-pager"],
        capture_output=True, text=True
    )
    return result.stdout

def get_network_interfaces():
    result = subprocess.run(["ip", "a"], capture_output=True, text=True)
    return result.stdout

def get_open_ports():
    result = subprocess.run(["ss", "-tulpn"], capture_output=True, text=True)
    return result.stdout

def collect_inventory():
    return {
        "disks": get_disks(),
        "block_devices": get_block_devices(),
        "docker_containers": get_docker_containers(),
        "docker_images": get_docker_images(),
        "services": get_services(),
        "network_interfaces": get_network_interfaces(),
        "open_ports": get_open_ports(),
    }

if __name__ == "__main__":
    inventory = collect_inventory()
    print(json.dumps(inventory, indent=2, ensure_ascii=False))
