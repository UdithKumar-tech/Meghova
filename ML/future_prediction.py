import pandas as pd
import joblib

# =========================
# 1. LOAD TRAINED MODELS
# =========================

classifier = joblib.load("regime_classifier.pkl")
encoder = joblib.load("regime_label_encoder.pkl")

experts = {
    "ACTIVE": joblib.load("experts/active_expert.pkl"),
    "BREAK": joblib.load("experts/break_expert.pkl"),
    "NORMAL": joblib.load("experts/normal_expert.pkl"),
    "DEPRESSION": joblib.load("experts/depression_expert.pkl"),
    "COASTAL_OROGRAPHIC": joblib.load(
        "experts/coastal_orographic_expert.pkl"
    )
}

# =========================
# 2. LOAD NEW NWP DATA
# =========================

df = pd.read_csv("data/future_nwp_input.csv")

df["VT"] = pd.to_datetime(df["VT"])
df["MONTH"] = df["VT"].dt.month

# =========================
# 3. FEATURES FOR CLASSIFIER
# =========================

classifier_features = [
    "LAT", "LON", "MONTH",
    "GH_850", "T_850", "RH_850", "U_850", "V_850",
    "TP_850", "CAPE_850",
    "GH_500", "T_500", "RH_500", "U_500", "V_500",
    "TP_500", "CAPE_500"
]

X_classifier = df[classifier_features]

# =========================
# 4. PREDICT WEATHER REGIME
# =========================

predicted_numbers = classifier.predict(X_classifier)

df["PREDICTED_REGIME"] = encoder.inverse_transform(
    predicted_numbers.astype(int)
)

# =========================
# 5. EXPERT FEATURES
# =========================

expert_features = [
    "LAT", "LON",
    "GH_850", "T_850", "RH_850", "U_850", "V_850",
    "TP_850", "CAPE_850",
    "GH_500", "T_500", "RH_500", "U_500", "V_500",
    "TP_500", "CAPE_500"
]

X_expert = df[expert_features]

# =========================
# 6. PREDICT CORRECTION
# =========================

df["PREDICTED_CORRECTION"] = 0.0

for regime, expert in experts.items():

    mask = df["PREDICTED_REGIME"] == regime

    if mask.sum() > 0:
        df.loc[mask, "PREDICTED_CORRECTION"] = expert.predict(
            X_expert.loc[mask]
        )

# =========================
# 7. CALCULATE MEGHOVA
# =========================

df["MEGHOVA_PREDICTED_RAINFALL"] = (
    df["TP_850"] + df["PREDICTED_CORRECTION"]
)

# Rainfall cannot be negative
df["MEGHOVA_PREDICTED_RAINFALL"] = (
    df["MEGHOVA_PREDICTED_RAINFALL"].clip(lower=0)
)

# =========================
# 8. SHOW RESULTS
# =========================

output_columns = [
    "VT",
    "LAT",
    "LON",
    "PREDICTED_REGIME",
    "TP_850",
    "PREDICTED_CORRECTION",
    "MEGHOVA_PREDICTED_RAINFALL"
]

print("\nMEGHOVA FUTURE PREDICTION")
print("=========================\n")

print(df[output_columns].to_string(index=False))

# =========================
# 9. SAVE PREDICTIONS
# =========================

df[output_columns].to_csv(
    "meghova_future_predictions.csv",
    index=False
)

print("\nPrediction saved to:")
print("meghova_future_predictions.csv")