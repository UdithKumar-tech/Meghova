from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class NWPInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    LAT: float
    LON: float
    VT: Optional[datetime] = None
    MONTH: Optional[int] = Field(default=None, ge=1, le=12)
    GH_850: float
    T_850: float
    RH_850: float
    U_850: float
    V_850: float
    TP_850: float
    CAPE_850: float
    GH_500: float
    T_500: float
    RH_500: float
    U_500: float
    V_500: float
    TP_500: float
    CAPE_500: float


class BatchPredictionRequest(BaseModel):
    rows: List[NWPInput]


class PredictionResult(BaseModel):
    latitude: float
    longitude: float
    valid_time: Optional[str]
    nwp_rainfall_mm: float
    predicted_regime: str
    predicted_correction_mm: float
    corrected_rainfall_mm: float
    rainfall_category: Optional[str] = None


class BatchPredictionResponse(BaseModel):
    results: List[PredictionResult]
    count: int


class HealthResponse(BaseModel):
    status: str
    model_ready: bool
    classifier_loaded: bool
    experts_loaded: int
    message: str
