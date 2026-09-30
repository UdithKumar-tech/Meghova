# MEGHOVA — Final Backend Package

FastAPI backend for the MEGHOVA SIH project. It implements the same ML pipeline documented in the team's ML branch:

NWP atmospheric inputs → XGBoost rainfall-regime classifier → regime-specific XGBoost expert → rainfall correction → corrected rainfall.

## 1. Important model note

The exact trained `.pkl` model artifacts are not bundled in this generated ZIP because binary model files were not available as mounted conversation files. The package includes `scripts/download_models.py`, which downloads the exact public model filenames used by the team's `aisha-ml` branch.

## 2. Run on Windows

Open PowerShell in this folder:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts\download_models.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or simply double-click `run.bat`.

API: `http://127.0.0.1:8000`
Swagger: `http://127.0.0.1:8000/docs`

## 3. Frontend connection

Set the frontend API base URL to:

```text
http://localhost:8000
```

The frontend can call:

- `GET /api/health`
- `GET /api/metadata`
- `POST /api/predict`
- `POST /api/predict/batch`
- `GET /api/predictions`

CORS is enabled for local development.

## 4. Prediction request

POST `/api/predict` with JSON shaped like `sample_request.json`.

The backend calculates the month from `VT` when `MONTH` is not supplied. The corrected rainfall formula matches the ML branch implementation:

`corrected_rainfall = max(0, TP_850 + predicted_correction)`

## 5. What this backend stores

Successful predictions are stored in local SQLite (`meghova.db`) so the frontend can display recent prediction history.

## 6. Production note

For deployment, change `CORS_ORIGINS` from `*` to the actual deployed frontend origin, and keep model files outside source control when appropriate.
