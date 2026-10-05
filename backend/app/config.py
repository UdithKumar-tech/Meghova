from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = Path(os.getenv("MEGHOVA_MODEL_DIR", BASE_DIR / "models"))
DB_PATH = Path(os.getenv("MEGHOVA_DB_PATH", BASE_DIR / "meghova.db"))
CORS_ORIGINS = [x.strip() for x in os.getenv("CORS_ORIGINS", "*").split(",") if x.strip()]

REGIME_MODEL = MODEL_DIR / "regime_classifier.pkl"
REGIME_ENCODER = MODEL_DIR / "regime_label_encoder.pkl"
EXPERT_DIR = MODEL_DIR / "experts"

REGIME_FEATURES = [
    "LAT", "LON", "MONTH",
    "GH_850", "T_850", "RH_850", "U_850", "V_850", "TP_850", "CAPE_850",
    "GH_500", "T_500", "RH_500", "U_500", "V_500", "TP_500", "CAPE_500",
]
EXPERT_FEATURES = [
    "LAT", "LON",
    "GH_850", "T_850", "RH_850", "U_850", "V_850", "TP_850", "CAPE_850",
    "GH_500", "T_500", "RH_500", "U_500", "V_500", "TP_500", "CAPE_500",
]
EXPERT_FILES = {
    "ACTIVE": EXPERT_DIR / "active_expert.pkl",
    "BREAK": EXPERT_DIR / "break_expert.pkl",
    "NORMAL": EXPERT_DIR / "normal_expert.pkl",
    "DEPRESSION": EXPERT_DIR / "depression_expert.pkl",
    "COASTAL_OROGRAPHIC": EXPERT_DIR / "coastal_orographic_expert.pkl",
}
