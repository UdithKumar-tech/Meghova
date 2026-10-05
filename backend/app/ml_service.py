from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from .config import EXPERT_FILES, EXPERT_FEATURES, REGIME_ENCODER, REGIME_FEATURES, REGIME_MODEL


class ModelNotReady(RuntimeError):
    pass


class MeghovaModel:
    def __init__(self) -> None:
        self.classifier = None
        self.encoder = None
        self.experts: dict[str, Any] = {}
        self.load_errors: list[str] = []
        self.reload()

    def reload(self) -> None:
        self.load_errors = []
        self.classifier = None
        self.encoder = None
        self.experts = {}
        try:
            self.classifier = joblib.load(REGIME_MODEL)
        except Exception as exc:
            self.load_errors.append(f"Could not load regime classifier: {exc}")
        try:
            self.encoder = joblib.load(REGIME_ENCODER)
        except Exception as exc:
            self.load_errors.append(f"Could not load regime label encoder: {exc}")
        for regime, path in EXPERT_FILES.items():
            try:
                self.experts[regime] = joblib.load(path)
            except Exception as exc:
                self.load_errors.append(f"Could not load {path.name}: {exc}")

    @property
    def ready(self) -> bool:
        return (
            self.classifier is not None
            and self.encoder is not None
            and set(self.experts) == set(EXPERT_FILES)
        )

    def health(self) -> dict:
        return {
            "status": "ok" if self.ready else "degraded",
            "model_ready": self.ready,
            "classifier_loaded": self.classifier is not None,
            "experts_loaded": len(self.experts),
            "message": "All MEGHOVA ML artifacts loaded." if self.ready else "; ".join(self.load_errors),
        }

    def _frame_from_rows(self, rows: list[dict]) -> pd.DataFrame:
        df = pd.DataFrame(rows)
        if "VT" in df.columns:
            df["VT"] = pd.to_datetime(df["VT"], errors="coerce")
        month = pd.to_numeric(df.get("MONTH"), errors="coerce") if "MONTH" in df else pd.Series(index=df.index, dtype=float)
        if "VT" in df.columns:
            month = month.fillna(df["VT"].dt.month)
        df["MONTH"] = month
        if df["MONTH"].isna().any():
            raise ValueError("Each input row needs MONTH or a valid VT date.")

        required = set(REGIME_FEATURES + EXPERT_FEATURES)
        missing = [c for c in required if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required field(s): {', '.join(sorted(missing))}")
        for col in required:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        numeric = df[REGIME_FEATURES + EXPERT_FEATURES]
        if numeric.isna().any().any():
            bad = numeric.columns[numeric.isna().any()].tolist()
            raise ValueError(f"Invalid/missing numeric values in: {', '.join(bad)}")
        return df

    def predict(self, rows: list[dict]) -> list[dict]:
        if not self.ready:
            raise ModelNotReady(self.health()["message"])
        df = self._frame_from_rows(rows)
        df["PREDICTED_REGIME"] = self.encoder.inverse_transform(
            self.classifier.predict(df[REGIME_FEATURES].astype(float)).astype(int)
        )
        df["PREDICTED_CORRECTION"] = 0.0
        for regime, group in df.groupby("PREDICTED_REGIME", sort=False):
            if regime not in self.experts:
                raise ValueError(f"No expert model available for predicted regime: {regime}")
            df.loc[group.index, "PREDICTED_CORRECTION"] = self.experts[regime].predict(
                group[EXPERT_FEATURES].astype(float)
            )
        df["CORRECTED_RAINFALL"] = (df["TP_850"] + df["PREDICTED_CORRECTION"]).clip(lower=0)
        results = []
        for _, row in df.iterrows():
            valid_time = pd.Timestamp(row["VT"]).isoformat() if pd.notna(row.get("VT")) else None
            results.append({
                "latitude": float(row["LAT"]),
                "longitude": float(row["LON"]),
                "valid_time": valid_time,
                "nwp_rainfall_mm": float(row["TP_850"]),
                "predicted_regime": str(row["PREDICTED_REGIME"]),
                "predicted_correction_mm": float(row["PREDICTED_CORRECTION"]),
                "corrected_rainfall_mm": float(row["CORRECTED_RAINFALL"]),
            })
        return results


model_service = MeghovaModel()
