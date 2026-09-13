const API_BASE = "";

async function checkHealth() {
    const el = document.getElementById("health-status");
    try {
        const response = await fetch(`${API_BASE}/api/health`);
        const data = await response.json();
        el.textContent = `Статус: ${data.status}`;
        el.classList.remove("error");
    } catch (error) {
        el.textContent = `Ошибка: ${error.message}`;
        el.classList.add("error");
    }
}

async function loadInventory() {
    const el = document.getElementById("inventory-output");
    el.textContent = "Загрузка...";
    try {
        const response = await fetch(`${API_BASE}/api/inventory`);
        const data = await response.json();
        el.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        el.textContent = `Ошибка: ${error.message}`;
    }
}

async function loadMonitor() {
    const el = document.getElementById("monitor-output");
    el.textContent = "Загрузка...";
    try {
        const response = await fetch(`${API_BASE}/api/monitor`);
        const data = await response.json();
        el.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        el.textContent = `Ошибка: ${error.message}`;
    }
}

document.addEventListener("DOMContentLoaded", () => {
    checkHealth();
    setInterval(checkHealth, 30000);
});
