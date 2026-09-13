from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from l0_inventory import collect_inventory
from l1_monitoring import collect_metrics
from l2_explanation import collect_explanations
from l3_recommendation import collect_recommendations

app = FastAPI(
    title="Media Server LORM",
    description="LORM-based decision support system for local media server",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/inventory")
def inventory():
    return collect_inventory()

@app.get("/api/monitor")
def monitor():
    return collect_metrics()

@app.get("/api/explain")
def explain():
    return collect_explanations()

@app.get("/api/recommend")
def recommend():
    return collect_recommendations()

frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.isdir(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
