# MEGHOVA Frontend

React + Vite frontend connected to the FastAPI backend.

## Run

```powershell
npm install
npm run dev
```

Backend must be running on `http://localhost:8000`.

Optional `.env`:

```text
VITE_API_BASE_URL=http://localhost:8000
```

## Pages

- Overview — live KPI cards, map, chart and verification summary
- Rainfall Map — interactive Karnataka map using backend predictions
- Forecast — 17-field NWP input form with supplied demo inputs
- Model Performance — time-based verification metrics
- Reports — prediction history stored by FastAPI in SQLite
- About — architecture and tech stack
