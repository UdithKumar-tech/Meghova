# Frontend API Contract

Use `http://localhost:8000` as the API base URL during local development.

## Health
GET `/api/health`

## Metadata
GET `/api/metadata`

## Single prediction
POST `/api/predict`

Body fields:
`LAT`, `LON`, optional `VT`, optional `MONTH`, `GH_850`, `T_850`, `RH_850`, `U_850`, `V_850`, `TP_850`, `CAPE_850`, `GH_500`, `T_500`, `RH_500`, `U_500`, `V_500`, `TP_500`, `CAPE_500`.

Response:
`latitude`, `longitude`, `valid_time`, `nwp_rainfall_mm`, `predicted_regime`, `predicted_correction_mm`, `corrected_rainfall_mm`.

## Batch prediction
POST `/api/predict/batch`

Body:
`{"rows": [ ...prediction objects... ]}`

## Prediction history
GET `/api/predictions?limit=50`
