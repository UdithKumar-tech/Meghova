# MEGHOVA — SIH26080 Final Integrated Project

This is the complete integrated package for the MEGHOVA SIH project.

## What is connected

```text
React + Vite frontend
        ↓ REST / Axios
FastAPI backend
        ↓
NWP input validation
        ↓
XGBoost regime classifier
        ↓
One of 5 regime-specific XGBoost experts
        ↓
Corrected rainfall
        ↓
Dashboard / Map / Forecast / Performance / Reports
```

## Folder structure

```text
MEGHOVA_FINAL/
├── frontend/                 # React + Vite UI
├── backend/                 # FastAPI + SQLite + model serving
│   ├── app/
│   ├── models/               # ACTUAL trained .pkl files
│   └── data/                 # demo NWP + verification data
├── ML/                       # original ML contribution/source/data/results
└── README.md
```

## Step 1 — Start backend

Windows PowerShell:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Check:

```text
http://127.0.0.1:8000/api/health
```

It should return `model_ready: true` and `experts_loaded: 5`.

Swagger:

```text
http://127.0.0.1:8000/docs
```

## Step 2 — Start frontend

Open a **second** terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal, normally:

```text
http://localhost:5173
```

The frontend already defaults to `http://localhost:8000`. If required, copy `.env.example` to `.env` and set `VITE_API_BASE_URL`.

## How the user tests it

1. Open **Forecast** from the sidebar.
2. Select one of the supplied demo NWP points.
3. The 17 model input fields are filled automatically.
4. Click **Run MEGHOVA Forecast**.
5. The request goes from React → FastAPI → real ML models.
6. The returned regime, correction and corrected rainfall are displayed.
7. The prediction is stored in SQLite and appears under **Reports**.
8. **Rainfall Map** displays the supplied future NWP points after MEGHOVA correction.
9. **Model Performance** displays the supplied time-based verification metrics.

## Important

The package contains the real trained model files from the supplied ML ZIP. No fake model or placeholder model is used for inference.

The UI's rainfall category is a deterministic category based on corrected rainfall amount. It should not be described as a trained probability score.

## Tech stack

- Frontend: React, Vite, React Router, Leaflet, Recharts, Axios
- Backend: Python, FastAPI, Pydantic, SQLite
- ML: XGBoost, scikit-learn, pandas, joblib
- API: REST/JSON

**Express.js is not used.**
