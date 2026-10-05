# MEGHOVA — FastAPI Backend

This backend is connected to the **actual trained MEGHOVA model artifacts** included in `backend/models/`.

## ML pipeline

`NWP atmospheric input → XGBoost regime classifier → regime-specific XGBoost expert → rainfall correction → corrected rainfall`

The classifier uses 17 features. The expert selected by the predicted regime uses the 16 atmospheric/location features documented in the ML branch.

## Run on Windows

Open PowerShell in `backend/`:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or run `run.bat`.

API: `http://127.0.0.1:8000`
Swagger: `http://127.0.0.1:8000/docs`

## Main endpoints

- `GET /api/health` — confirms all 6 model artifacts are loaded.
- `GET /api/metadata` — model features and pipeline.
- `GET /api/demo-inputs` — supplied future NWP demo rows.
- `POST /api/forecast` — run one real ML prediction.
- `POST /api/forecast/batch` — run multiple predictions.
- `GET /api/forecast/map` — predictions for the supplied demo points.
- `GET /api/verification` — supplied time-based verification metrics.
- `GET /api/predictions` — recent predictions stored in SQLite.

`/api/predict` and `/api/predict/batch` are retained as compatibility aliases.

## Model files

The final package includes:

```text
models/
├── regime_classifier.pkl
├── regime_label_encoder.pkl
└── experts/
    ├── active_expert.pkl
    ├── break_expert.pkl
    ├── coastal_orographic_expert.pkl
    ├── depression_expert.pkl
    └── normal_expert.pkl
```

## Formula

`corrected_rainfall = max(0, TP_850 + predicted_correction)`

The rainfall category shown in the UI is derived from the corrected rainfall amount; it is not a separately trained probability model.
