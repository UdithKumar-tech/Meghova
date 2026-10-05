from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .config import CORS_ORIGINS, EXPERT_FILES, EXPERT_FEATURES, REGIME_FEATURES
from .database import recent_predictions, save_predictions
from .ml_service import ModelNotReady, model_service
from .schemas import BatchPredictionRequest, BatchPredictionResponse, HealthResponse, NWPInput

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

app = FastAPI(
    title="MEGHOVA API",
    version="2.0.0",
    description="FastAPI service for MEGHOVA regime-aware rainfall post-processing.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if CORS_ORIGINS == ["*"] else CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _load_demo_inputs() -> list[dict[str, Any]]:
    path = DATA_DIR / "future_nwp_input.csv"
    if not path.exists():
        return []
    df = pd.read_csv(path)
    return df.where(pd.notna(df), None).to_dict(orient="records")


def _risk_label(mm: float) -> str:
    if mm >= 150:
        return "Extreme"
    if mm >= 100:
        return "Very Heavy"
    if mm >= 64.5:
        return "Heavy"
    if mm >= 15.6:
        return "Moderate"
    if mm >= 2.5:
        return "Light"
    return "Very Light"


@app.get("/api")
def root():
    return {
        "name": "MEGHOVA API",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/api/health",
        "forecast": "POST /api/forecast",
        "map": "GET /api/forecast/map",
    }


@app.get("/api/health", response_model=HealthResponse)
def health():
    return model_service.health()


@app.get("/api/metadata")
def metadata():
    return {
        "project": "MEGHOVA",
        "pipeline": [
            "NWP atmospheric input",
            "rainfall regime classification",
            "regime-specific XGBoost bias correction",
            "corrected rainfall = max(0, NWP + correction)",
        ],
        "regimes": sorted(EXPERT_FILES.keys()),
        "regime_features": REGIME_FEATURES,
        "expert_features": EXPERT_FEATURES,
        "model_ready": model_service.ready,
    }


@app.get("/api/demo-inputs")
def demo_inputs():
    rows = _load_demo_inputs()
    return {"items": rows, "count": len(rows)}


def _predict(rows: list[dict[str, Any]]):
    results = model_service.predict(rows)
    for result in results:
        result["rainfall_category"] = _risk_label(result["corrected_rainfall_mm"])
    return results


@app.post("/api/forecast")
def forecast(payload: NWPInput):
    try:
        results = _predict([payload.model_dump()])
        created_at = datetime.now(timezone.utc).isoformat()
        save_predictions(results, created_at)
        return results[0]
    except ModelNotReady as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}")


@app.post("/api/predict")
def predict_alias(payload: NWPInput):
    return forecast(payload)


@app.post("/api/forecast/batch", response_model=BatchPredictionResponse)
def forecast_batch(payload: BatchPredictionRequest):
    if not payload.rows:
        raise HTTPException(status_code=422, detail="rows cannot be empty")
    try:
        results = _predict([r.model_dump() for r in payload.rows])
        created_at = datetime.now(timezone.utc).isoformat()
        save_predictions(results, created_at)
        return {"results": results, "count": len(results)}
    except ModelNotReady as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {exc}")


@app.post("/api/predict/batch", response_model=BatchPredictionResponse)
def predict_batch_alias(payload: BatchPredictionRequest):
    return forecast_batch(payload)


@app.get("/api/forecast/map")
def forecast_map():
    try:
        rows = _load_demo_inputs()
        if not rows:
            return {"locations": [], "count": 0}
        results = _predict(rows)
        locations = [
            {
                "lat": r["latitude"],
                "lon": r["longitude"],
                "rainfall": r["corrected_rainfall_mm"],
                "nwp_rainfall": r["nwp_rainfall_mm"],
                "corrected_rainfall": r["corrected_rainfall_mm"],
                "regime": r["predicted_regime"],
                "date": r["valid_time"],
                "category": r["rainfall_category"],
            }
            for r in results
        ]
        return {"locations": locations, "count": len(locations)}
    except ModelNotReady as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Map forecast failed: {exc}")


@app.get("/api/verification")
def verification():
    path = DATA_DIR / "results" / "meghova_time_based_rainfall_metrics.csv"
    if not path.exists():
        return {"available": False, "metrics": []}
    df = pd.read_csv(path)
    rows = df.where(pd.notna(df), None).to_dict(orient="records")
    return {"available": True, "metrics": rows, "count": len(rows)}


@app.get("/api/predictions")
def get_predictions(limit: int = Query(default=50, ge=1, le=500)):
    items = recent_predictions(limit)
    return {"items": items, "count": len(items)}


@app.post("/api/models/reload")
def reload_models():
    model_service.reload()
    return model_service.health()
