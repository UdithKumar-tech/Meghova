from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .config import CORS_ORIGINS, EXPERT_FILES, EXPERT_FEATURES, REGIME_FEATURES
from .database import recent_predictions, save_predictions
from .ml_service import ModelNotReady, model_service
from .schemas import HealthResponse, BatchPredictionRequest, BatchPredictionResponse, NWPInput

app = FastAPI(
    title='MEGHOVA Backend API',
    version='1.0.0',
    description='FastAPI backend for MEGHOVA NWP post-processing and rainfall correction.',
)

allow_origins = ['*'] if CORS_ORIGINS == ['*'] else CORS_ORIGINS
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/api/health', response_model=HealthResponse)
def health():
    return model_service.health()


@app.get('/api/metadata')
def metadata():
    return {
        'project': 'MEGHOVA',
        'pipeline': [
            'NWP atmospheric input',
            'rainfall regime classification',
            'regime-specific bias correction',
            'NWP rainfall + correction',
        ],
        'regimes': sorted(EXPERT_FILES.keys()),
        'regime_features': REGIME_FEATURES,
        'expert_features': EXPERT_FEATURES,
        'formula': 'corrected_rainfall = max(0, TP_850 + predicted_correction)',
        'model_ready': model_service.ready,
    }


@app.post('/api/predict')
def predict(payload: NWPInput):
    try:
        results = model_service.predict([payload.model_dump()])
        created_at = datetime.now(timezone.utc).isoformat()
        save_predictions(results, created_at)
        return results[0]
    except ModelNotReady as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f'Prediction failed: {exc}')


@app.post('/api/predict/batch', response_model=BatchPredictionResponse)
def predict_batch(payload: BatchPredictionRequest):
    if not payload.rows:
        raise HTTPException(status_code=422, detail='rows cannot be empty')
    try:
        results = model_service.predict([r.model_dump() for r in payload.rows])
        created_at = datetime.now(timezone.utc).isoformat()
        save_predictions(results, created_at)
        return {'results': results, 'count': len(results)}
    except ModelNotReady as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f'Batch prediction failed: {exc}')


@app.post('/api/models/reload')
def reload_models():
    model_service.reload()
    return model_service.health()


@app.get('/api/predictions')
def get_predictions(limit: int = Query(default=50, ge=1, le=500)):
    return {'items': recent_predictions(limit), 'count': len(recent_predictions(limit))}


@app.get('/api')
def root():
    return {
        'name': 'MEGHOVA Backend API',
        'docs': '/docs',
        'health': '/api/health',
        'predict': 'POST /api/predict',
        'batch_predict': 'POST /api/predict/batch',
    }
